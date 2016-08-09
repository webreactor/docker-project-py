from setuptools import setup
from setuptools import find_packages


setup(
    name="docker-project",
    version="0.0.1",
    install_requires=[
        'PyYAML >= 3.10, < 4'
    ],
    entry_points={
        'console_scripts': [
            'docker-project = docker_project.cli_controller:main',
        ],
    },
    packages=find_packages()
)
