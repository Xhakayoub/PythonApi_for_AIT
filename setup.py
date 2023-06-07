from setuptools import setup

with open('requirements.txt', 'r') as file:
    requirements = file.read().splitlines()

setup(
    name='AiTransfert',
    version='1.0.0',
    description='AI for Football',
    author='Mouissi Ayoub',
    packages=['AiTransfert'],
    install_requires=requirements,

)