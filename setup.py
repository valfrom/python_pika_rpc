
from setuptools import setup, find_packages

setup(
    name='pika_rpc',
    version='0.1.8',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Pika RPC python package',
    long_description=open('README.md').read(),
    install_requires=['pillow', 'numpy'],
    url='https://github.com/valfrom/python_pika_rpc',
    author='Valerii Ivanov',
    author_email='valfrom@gmail.com'
)
