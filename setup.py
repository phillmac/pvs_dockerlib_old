import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='pvs_dockerlib',  
    version='0.1',
    #scripts=['dockerlib'] ,
    author="Peel Valley Softwware",
    author_email="info@peelvalley.com.au",
    description="Custom docker client wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/phillmac/DockerLib",
    packages=setuptools.find_packages(),
    install_requires=[
   'docker',
    ],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
