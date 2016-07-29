# import yaml
import path from os

class loader():
    config = {}
    def __init__(self, filename = None):
        if filename != None:
            self.load(filename)

    def load(self, filename):
        config = self.load_file(filename)
        config['_source'] = filename
        self.resolveExtends()
        

    def load_file(self, filename):
        print("load yml: " + filename)
        self.verify_config(config)

        # with open(filename, 'r') as stream:
        #     return yaml.load(stream)


    def verify_config(config):
        if version not in config or config['version'] != 2:
            print("version 2 is only supported at file " + config['_source']);
        if "service" not in config:
            print("no services defined at file " + config['_source']);
        return true

    # def normalize(config):
    #     for service_name, service in config['services']:
    #         service['_service_name'] = service_name

    def resolveExtends(config):
        config_path = path.dirname(config['_source'])
        for service in config['services']:
            service['_source'] = config['_source']
            if "extends" in service and file in service['extends']:
                extends = service['extends']
                extends_file = self.normalizePath(extends['file'], config_path)
                if path.is_file(extends_file):
                    

        foreach ($config['services'] as $service_name => $service) {
            $config['services'][$service_name]['_source'] = $config['_source'];
            if (isset($service['extends'])) {
                $extends = $service['extends'];
                $extends_file = Utilities::normalizePath($extends['file'], $pwd);
                if (is_file($extends_file)) {
                    $extention_data = $this->loadFile($extends_file);
                    if (isset($extention_data['services'][$extends['service']])) {
                        $service_extention = $extention_data['services'][$extends['service']];
                        $service_extention['_source'] = $extention_data['_source'];
                        $config['services'][$service_name] = Utilities::mergeRecursive(
                            $config['services'][$service_name],
                            $service_extention
                        );
                    }
                } else {
                    echo "Warning: [$service_name] $extends_file does not exist\n";
                }
            }
        }
        return $config;

