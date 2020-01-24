import yaml


class AppSettings:

    @staticmethod
    def get_settings():
        with open(r'settings.yaml') as file:
            settings_dict = yaml.load(file, Loader=yaml.FullLoader)
        return settings_dict
