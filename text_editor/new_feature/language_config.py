import configparser

class LanguageConfig:
    def __init__(self, config_file="languages.cfg"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_supported_languages(self):
        if 'languages' in self.config:
            return self.config['languages']
        else:
            return {}
