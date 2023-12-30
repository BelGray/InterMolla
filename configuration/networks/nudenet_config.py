import io
from nudenet import NudeClassifier
import disnake
from configuration.tool import config_manager
from configuration.tool.logger import log
class NudenetConfig:
    def __init__(self, vulgar_if_more_than: float):
        self.__nude_cls = NudeClassifier()
        self.__vulgar = vulgar_if_more_than if 0 <= vulgar_if_more_than <= 1.0 else 0.90
    async def is_vulgar(self, unique_filename: str) -> bool:
        path = 'attachments/' + unique_filename
        res = self.__nude_cls.classify(path)
        result = res[str(path)]['unsafe']
        log.i(f'is_vulgar. unique_filename: {unique_filename}', f'Unsafe result: {result} [{self.__vulgar}]')
        return True if result >= self.__vulgar else False

