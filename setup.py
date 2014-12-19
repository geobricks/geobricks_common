from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksCore',
    version='0.0.1',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks core library.',
    install_requires=[],
    url='http://pypi.python.org/pypi/GeobricksCore/',
    keywords=['geobricks']
)
