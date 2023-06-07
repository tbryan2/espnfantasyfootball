from setuptools import setup

setup(
    name='espnfantasyfootball',
    version='0.1.1',
    description='A Python package to interact with ESPN Fantasy Football data',
    url='https://github.com/tbryan2/espnfantasyfootball',
    author='Tim Bryan',
    license='MIT',
    packages=['espnfantasyfootball'], 
    install_requires=['requests', 'pandas']
)