import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='pvs-dockerlib',  
    version='0.0.2',
    author="Peel Valley Softwware",
    author_email="info@peelvalley.com.au",
    description="Custom docker client wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
