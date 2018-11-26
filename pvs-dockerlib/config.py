import os

class DockerConfig():

    def __init__(self):
        pass

    def base_url(self):
        if 'DOCKER_BASE_URL' in os.environ and not os.environ['DOCKER_BASE_URL'] == '' :
            return os.environ['DOCKER_BASE_URL']
        else:
            return 'unix:///var/run/docker.sock'

    def version(self):
        if  'DOCKER_VERSION' in os.environ and not os.environ['DOCKER_VERSION'] == '':
            return os.environ['DOCKER_VERSION']
        else:
            return 'auto'

    def timeout(self):
        if 'DOCKER_TIMEOUT' in os.environ and not os.environ['DOCKER_TIMEOUT'] == '':
            return int(os.environ['DOCKER_TIMEOUT'])
        else:
            return 120