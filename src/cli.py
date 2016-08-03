#!/usr/bin/env python3
import os.path
import sys

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

import docker_project.cli_controller
import docker_project.logic.main
import argparse

app = docker_project.logic.main.Application()
cli = docker_project.cli_controller.CliController(app)

cli.handle(argparse.ArgumentParser("docker-project"))