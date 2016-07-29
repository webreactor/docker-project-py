import argparse


class cli_controller():
    parser = argparse.ArgumentParser("docker project management tool 0.0.1")

    def get_config(self):

        self.parser.add_argument("command",
                            default="help",
                            help="command to run")

        self.parser.add_argument("-f", "--file",
                            default="docker-compose.yml",
                            dest="file",
                            help="Config file")

        self.parser.add_argument("-a", "--apps",
                            default="apps",
                            dest="apps",
                            help="Applications sources folder")

        self.parser.add_argument("-x", "--extra",
                            default="apps",
                            dest="apps",
                            help="Extra parameters passed to a command")
        return self.parser.parse_args()


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