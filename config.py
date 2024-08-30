import yaml
from singletone import SingletonInstane

class ConfigInfo(SingletonInstane):
    def __init__(self):
        self.LoadConfig()
        self.LoadSecurity()
    
    def LoadConfig(self):
        with open('config.yaml') as f:
            config_data = yaml.load(f, Loader=yaml.FullLoader)
            self.db_path = config_data['db_path']
            self.polling_sec = config_data['polling_sec']
            

    def LoadSecurity(self):
        with open('security.yaml') as s:
            security_data = yaml.load(s, Loader=yaml.FullLoader)
            self.discord_hook = security_data['discord_hook']
            self.telegram_token = security_data['telegram_token']
            self.telegram_chat_id = security_data['telegram_chat_id']

    def ReloadAll(self):
        self.LoadConfig()
        self.LoadSecurity()
