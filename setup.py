import os
from setuptools import setup, find_packages
from pip.req import parse_requirements


def read(filename):
    """Read a file and return its contents.
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as infile:
        content = infile.read()

    return content


setup(
    name="Text_Metrics",
    version="0.0.1",
    author="Nathan Siegle Hartmann",
    author_email="nathanshartmann@gmail.com",
    keywords="text complexity metrics",
    # url="http://packages.python.org/????",
    packages=find_packages(),
    # long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Natural Language :: Portuguese (Brazilian)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
    ],
    #install_requires = [str(ir.req)
    #                    for ir in parse_requirements('requirements.txt')]
)
