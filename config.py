from dataclasses import dataclass
import yaml # pip install PyYAML
import json # comes with Python
import toml # pip install toml or pip install tomlkit

@dataclass
class Application:
    name: str
    input_type: str
    path: str

# Make this cooler
class Config:

    def __init__(self, target_file, is_yaml=False, is_json=False, is_toml=False):
        self.file = target_file
        self.applications = []
        self.is_yaml = is_yaml
        self.is_toml = is_toml
        self.is_json = is_json
        if is_yaml:
            self.loadYamlConfigs()
        elif is_toml:
            self.loadTomlConfigs()
        elif is_json:
            self.loadJsonConfigs()

    def loadYamlConfigs(self):
        with open(self.file, 'r') as file:
            self.config = yaml.safe_load(file)
        # print(self.config)

    def loadTomlConfigs(self):
        with open(self.file, 'r') as file:
            self.config = toml.load(file)
        # print(self.config)

    def loadJsonConfigs(self):
        with open(self.file, 'r') as file:
            self.config = json.load(file)
        # print(self.config)

    def addApplication(self, name, input_type, path):
        self.applications.append(Application(name=name, input_type=input_type, path=path))

    def parseConfigs(self):
        self.applications = []
        self.name = self.config['app']['name']
        for app in self.config['applications']:
            self.applications.append(Application(name=app['name'], input_type=app['input_type'], path=app['path']))

    def updateConfig(self):
        applications = []
        for app in self.applications:
            applications.append({
                "name": app.name,
                "input_type": app.input_type,
                "path": app.path
            })
        config = {
            "app": {
                "name": self.name,
            },
            "applications": applications,
            "test": {
                "cool": True
            }
        }

        if self.is_yaml:
            self.writeToYaml(config)
        elif self.is_toml:
            self.writeToToml(config)
        elif self.is_json:
            self.writeToJson(config)

    def writeToYaml(self, config):
        with open(self.file, 'w') as file:
            yaml.dump(config, file)

    def writeToToml(self, config):
        with open(self.file, 'w') as file:
            toml.dump(config, file)

    def writeToJson(self, config):
        with open(self.file, 'w') as file:
            json.dump(config, file, indent=4)

    def __str__(self):
        toReturn = f"Name: {self.name}\n"
        toReturn += f"Applications: {self.applications}"
        return toReturn

# config = Config("config.yaml", is_yaml=True)
# # config = Config("config.json", is_json=True)
# # config = Config("config.toml", is_toml=True)

# config.parseConfigs()
# config.addApplication("Hi YouTube", "file", "C:\\cool")
# # print(config)
# config.updateConfig()
