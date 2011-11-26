import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
 
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README')

setup(
    name = "pynfsn",
    version = "0.1",
    url = 'http://github.com/goncalopp/pyNFSN',
    license = 'CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    description = "Module for NearlyFreeSpeech.net RESTful API",
    long_description = README,
    author = 'Goncalo Pinheira',
    author_email = 'goncalopp@gmail.com',
    packages = ['pynfsn'],
    classifiers = \
        [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        ]
)
