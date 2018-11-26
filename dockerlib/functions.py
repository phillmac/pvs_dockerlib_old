from docker.errors import APIError, NotFound
from requests import ConnectionError
from .config import DockerConfig
import docker, threading



def create_client():
    _config = DockerConfig()
    return docker.DockerClient(
        base_url = _config.base_url(),
        version = _config.version(),
        timeout = _config.timeout()
    )

def docker_run_settings(docker_client, docker_settings):
    if 'ports' in docker_settings:
        for port_mapping, value in docker_settings['ports'].items():
            docker_settings['ports'][port_mapping] = tuple(value)
    return docker_client.containers.run(**docker_settings)


def docker_start_settings(docker_client, docker_settings):
    container_name = docker_settings['name']
    print('Starting container: ', container_name)
    if len(docker_client.containers.list(all=True, sparse=True, filters={'name':container_name})) > 0:
        print('Found container')
        container = docker_client.containers.get(container_name)
        container.start()
        print('Started')
        return True
    else:
        print('Container not found, creating')
        docker_run_settings(docker_client, docker_settings)
        return True

def docker_stop_settings(docker_client, docker_settings):
    container_name = docker_settings['name']
    if len(docker_client.containers.list(all=True, sparse=True, filters={'name':container_name})) > 0:
        container = docker_client.containers.get(container_name)
        container.stop(timeout=60)
        container.wait(
            timeout = 70,
            condition = 'not-running'
        )
        return True
    return False

def docker_restart_settings(docker_client, docker_settings):
    container_name = docker_settings['name']
    if len(docker_client.containers.list(all=True, sparse=True, filters= {'name':container_name})) > 0:
        container = docker_client.containers.get(container_name)
        container.restart(timeout=60)
        """ container.wait(
            timeout = 30,
            condition = 'not-running'
        ) """
        return True
    else:
        docker_run_settings(docker_client, docker_settings)
        return True

def docker_remove_settings(docker_client, docker_settings):
    container_name = docker_settings['name']
    print('Finding container: ', container_name)
    if len(docker_client.containers.list(all=True, sparse=True, filters= {'name':container_name})) > 0:
        container = docker_client.containers.get(container_name)
        if container:
            print('Found container')
            event = threading.Event()
            wait_ready = threading.Event()
            t = threading.Thread(target=wait_container_status, args = (create_client(), docker_settings,'removed',wait_ready,event,10))
            t.daemon = True
            t.start()
            wait_ready.wait()
            container.remove(force=True)
            print('Waiting...')
            event.wait()
            print('Removed container')
    return False

def container_get_status(docker_client, docker_settings):
    container_name = docker_settings['name']
    try:
        container = find_container(docker_client, container_name)
        return container.status
    except NotFound:
        return 'CONTAINER_NOT_FOUND'


def docker_logs_settings(docker_client, docker_settings):
    container_name = docker_settings['name']
    try:
        container = find_container(docker_client, container_name)
        return container.logs(stdout=True, stderr=True, tail=10)
    except NotFound:
        return 'Container not found'


def wait_container_status(docker_client, docker_settings, condition, wait_ready, status_achieved, timeout=10, tries=0):
    
    if not status_achieved:
        raise ValueError('status_achieved must not be null')

    container_name = docker_settings['name']
    try:
        container = find_container(docker_client, container_name)

        if wait_ready and not wait_ready.is_set():
            wait_ready.set()
        container.wait(timeout=timeout,condition=condition)
        status_achieved.set()
    except ConnectionError as ex:
        if tries < 3:
            tries += 1
            wait_container_status(docker_client, docker_settings, condition, wait_ready, status_achieved, timeout, tries)
        else:
            raise ex
    except NotFound as ex:
        if condition == 'removed':
            status_achieved.set()
        else:
            raise ex



def find_container(docker_client, container_name):
    print('Finding container: ', container_name)
    if len(docker_client.containers.list(all=True, sparse=True, filters= {'name':container_name})) > 0:
        return docker_client.containers.get(container_name)
    else:
        raise NotFound('No containers with name {container_name} available.'.format(**locals()))
