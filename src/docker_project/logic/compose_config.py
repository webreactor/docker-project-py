import os
import yaml
from . import utilities

class ComposerConfig():
    config = {}

    def __init__(self, filename = None):
        if filename != None:
            self.load(filename)

    def open(self, filename):
        self.config = self.load(filename)

    def load(self, filename):
        config = self.load_yml_file(filename)
        config['_source'] = filename
        self.verify(config)
        self.normalize(config)
        self.resolve_extends(config)
        return config

    def load_yml_file(self, filename):
        try:
            if not os.path.isfile(filename):
                raise Exception("file does not exist")
            with open(filename, 'r') as stream:
                return yaml.load(stream)
        except Exception as e:
            raise Exception("Failed loading '"+ filename+ "': " + str(e))

    def normalize(self, config):
        for service_name, service in config['services'].items():
            if "labels" not in service:
                service["labels"] = {}
            if "image" not in service:
                service["image"] = None

    def verify(self, config):
        if "version" not in config and config["version"] != 2:
            raise Exception("version 2 is only supported at file " + config['_source']);
        if "services" not in config:
            raise Exception("no services defined at file " + config['_source']);
        return True

    def resolve_extends(self, config):
        config_path = os.path.dirname(config['_source'])
        for service_name in list(config['services']):
            service = config['services'][service_name]
            service['_source'] = config['_source']
            if "extends" in service and "file" in service['extends']:
                extends = service['extends']
                extends_file = utilities.normalize_path(extends['file'], config_path)
                extends_service_name = extends['service']
                if os.path.isfile(extends_file):
                    extends_data = self.load(extends_file)
                    if extends_service_name in extends_data['services']:
                        service_extention = extends_data['services'][extends_service_name]
                        service_extention['_source'] = extends_data['_source']
                        config['services'][service_name] = utilities.merge_dict_recursive(
                                config['services'][service_name],
                                service_extention)
                else:
                    print("Warning: [{}] {} does not exist".format(service_name, extends_file))
        return config

    def get_service(self, name):
        return self.config['services'][name]

    def get_services(self):
        return self.config['services']

    def get_service_label(self, service_name, label_name):
        service = self.get_service(service_name)
        if label_name in service['labels']:
            return service['labels'][label_name]
        return None
