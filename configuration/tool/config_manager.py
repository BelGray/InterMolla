import enum
import os.path
import json
from BGLogger import BGC
from configuration.tool.logger import log

class Admin:
    __trusted_users = (685578986784686116, 1072379692318998598)
    __channels = {
        'attachments': 1078429568572080243,
        'news': {
            'ru': 1078429568148439057,
            'en': 1092207387659730974
        },
        'rules': 1078429568148439058,
        'logs': {
            'ru': 1086310760034074664,
            'en': 1092207696989667348
        },
        'welcome': 1092196394632216627,
        'shop': {
            'ru': 1078429568572080238,
            'en': 1092207864560484543
        },
        'system': 1087455065125699656,
        'requests': {
            'post': 1078429568572080244,
            'add': 1078429568572080245
        },
        'chat': {
            'ru': 1078429568945361009,
            'en': 1092208016134258758
        },
        'feedbacks': {
            'ru': 1078429568945361015,
            'en': 1092208923194445935
        },
        'complaints': {
            'ru': 1078429568945361016,
            'en': 1092209489664544898
        },
        'ideas': {
            'ru': 1078429569255735308,
            'en': 1092209553946456166
        },
        'bugs': {
            'ru': 1078429569255735309,
            'en': 1092209707416047637
        }
    }

    @staticmethod
    def channels():
        return Admin.__channels



    @staticmethod
    def user_is_trusted(discord_id: int):
        if discord_id in Admin.__trusted_users:
            return True
        return False

class Services(enum.Enum):
    DISCORD = "discord_api_token"
    QIWI = "qiwi_api_token"
    PERSPECTIVE = "perspective_api_token"

class ConfigManager:
    @staticmethod
    def init_bot_config():
        if not os.path.exists('bot_config.json'):
            with open('bot_config.json', 'w') as f:
                f.write('''{"inter_molla":{"config":{"discord_api_token":null, "qiwi_api_token":null}}}''')
                f.close()
            log.s('init_bot_config', 'created new config file (bot_config.json)')
            return
        log.w('init_bot_config', 'bot_config.json already exists')

    @staticmethod
    def set_api_token(service: Services, token: str):
        with open("bot_config.json", 'r') as f:
            loader = json.load(f)
            f.close()
        with open("bot_config.json", 'w') as f:
            loader["inter_molla"]["config"][service.value] = token
            json.dump(loader, f)
            f.close()

    @staticmethod
    def get_api_token(service: Services):
        with open("bot_config.json", 'r') as f:
            loader = json.load(f)
            f.close()
        if loader["inter_molla"]["config"][service.value] != None:
            return loader["inter_molla"]["config"][service.value]
        new_token = BGC.scan(label=f"В файле конфигурации bot_config.json отсутствует API токен ({service.value}). Введите токен здесь /> ",
                             label_color=BGC.Color.CRIMSON)
        ConfigManager.set_api_token(service, new_token)
        return new_token

