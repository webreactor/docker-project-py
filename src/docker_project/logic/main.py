
import os
from . import utilities
from . import compose_config
import re

class Application():

    apps = {}

    def init_apps_dir(self, path):
        self.apps_dir = path
        if not os.path.isdir(path):
            os.mkdir(path, 0o766)

    def load_compose_file(self, file):
        self.config = compose_config.Loader()
        self.config.open(file)
        self.apps = self.parse_app_dirs(self.config)

    def run_update(self, extra):
        for service_name, app_dir in self.apps:
            git_link = self.config.get_service_label(service_name, 'project.git')
            if git_link is not None:
                branch = self.config.get_service_label(service_name, 'project.git.branch')
                if branch is None:
                    branch = 'master'
                self.git_update(service_name, git_link, branch, extra)

    def git_update(self, service_name, link, branch, extra):
        if os.path.isdir(self.apps[service_name] + ".git"):
            self.exec_for_service(
                "git clone {} -b {} {} .".format(extra, branch, link), 
                service_name)
        else:
            self.exec_for_service(
                "git pull {}".format(extra),
                service_name)

    def exec_for_service(self, command, service_name):
        path = self.apps[service_name]
        print("--------------------------------------------");
        print("Service: {} as {}".format(service_name, path));
        command.format(service=service_name, image=service['image'])
        utilities.exec_shell(command, path)

    def run_shell(self, command_name, extra):
        for service_name, app_dir in self.apps:
            self.exec_for_service(extra, service_name)

    def run_project_command(self, command_name, extra):
        label = "project.{}".format(command_name).lower()
        for service_name, app_dir in self.apps:
            command = self.config.get_service_label(service_name, label)
            if command is not None:
                self.exec_for_service(command + " " + extra, service_name)

    def parse_app_dirs(self, config):
        apps = {}
        for service_name in config.get_services():
            service = config.get_service(service_name)
            path = None
            if "build" in service:
                path = service['build']
            git_link = config.get_service_label(service_name, "project.git")
            if git_link is not None:
                m = re.search("([\w\-]+\/[\w\-]+)\.git", git_link)
                if m is not None:
                    path = m.group(1)
            if path is not None:
                apps[service_name] = utilities.normalize_path(path, os.path.dirname(service['_source']))
        return apps
