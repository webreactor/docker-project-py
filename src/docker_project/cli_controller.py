
import os
from .logic import utilities
import re

class CliController():

    def __init__(self, app):
        self.app = app
        self.config = {}
        self.pwd = os.getcwd()

    def define_arguments(self, arguments_container):
        arguments_container.add_argument("command",
                            default="help",
                            help="command to run")

        arguments_container.add_argument("-f", "--file",
                            default="docker-compose.yml",
                            dest="file",
                            help="Config file")

        arguments_container.add_argument("-a", "--apps",
                            default="apps",
                            dest="apps",
                            help="Applications sources folder")

        arguments_container.add_argument("-x", "--extra",
                            default=None,
                            dest="extra",
                            help="Extra parameters to be passed to a command")
        return vars(arguments_container.parse_args())

    def get_arguments(self, arguments_container):
        raw = self.define_arguments(arguments_container)
        arguments = {}
        arguments["composer-file"] = utilities.normalize_path(raw["file"], self.pwd)
        arguments["apps-dir"] = utilities.normalize_path(raw["apps"], self.pwd)
        arguments["command"] = raw["command"]
        arguments["extra"] = raw["extra"]
        return arguments

    def handle(self, arguments_container):
        try:
            self.handle_logic(arguments_container)
        except Exception as e:
            print("Error: " + str(e))
            raise e

    def handle_logic(self, arguments_container):
        arguments = self.get_arguments(arguments_container)
        self.app.init_apps_dir(arguments['apps-dir'])
        command = arguments['command'].lower()
        try:
            handler = getattr(self, "run_" + command)
        except AttributeError as e:
            handler = self.project_command
        handler(arguments)


    def run_help(self, arguments):
        pass

    def project_command(self, arguments):
        pass
    def run_status(self, arguments):
        self.app.load_compose_file(arguments['composer-file'])
        print("Compose file: " + arguments['composer-file'])
        print("Apps folder:  " + arguments['apps-dir'])
        if arguments['extra'] is not None:
            print("Extra parameters: {$arguments['extra']}")
        print("\nRegistered services")
        label_check = re.compile("^project.(.+)$")
        for service_name in self.app.apps:
            app_dir = self.app.apps[service_name]
            print(service_name + ":")
            print("  Application folder: " + app_dir)
            service = self.app.config.get_service(service_name)
            for key in service['labels']:
                label = service['labels'][key]
                m = label_check.match(key)
                if m is not None:
                    print("  " + m.group(1) + ": " + label)
            print("")
    def run_update(self, arguments):
        pass
    def run_shell(self, arguments):
        pass


# Commands:
#   update - clones or pulls application source
#   shell - uses extra parameter to run shell command for each app
#   status - prints current services with repos and their commands
#   help - prints help
#   your_command - defined as label for the service (example: labels: PROJECT_TEST: make test)

# Arguments:
#   Full name        | Short | Default          | Note
# -----------------------------------------------------
#   --file             -f      docker-compose.yml Alternative config file
#   --apps             -a      apps               Applications sources folder
#   --extra            -x                         Extra parameters passed to command