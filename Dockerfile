FROM phillmac/python-ubuntu

COPY . /src
RUN cd /src && python setup.py bdist_wheel