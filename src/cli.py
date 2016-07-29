#!/usr/bin/env python3

import docker_project.cli_controller
import os.path
import sys

parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

import pureyaml


cli = docker_project.cli_controller.cli_controller()

print(cli.get_config().command)
