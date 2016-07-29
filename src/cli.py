#!/usr/bin/env python3

import docker_project.cli_controller
cli = docker_project.cli_controller.cli_controller()

print(cli.get_config().command)
