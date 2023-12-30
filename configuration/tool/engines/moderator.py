import enum
import os
import disnake
from configuration.tool.engines.attachment_manager import att_man
class Model(enum.Enum):
    NSFW = "nsfw"
    OFFENSES = "offenses"

class AutoModeration:
    def __init__(self):
        self.offensive_expressions = ("идиот", "даун", "долбоёб", "еблан", "ебанат", "гондон", "пидор", "подонок", "говнюк", "сучара", "шмара", "шваль", "уёбок", "безмамыш", "безмамный", "мразь", "мудак", "ебалай") #Писать это всё противно было))
        self.__placeholder = {
  'а' : ['а', 'a', '@'],
  'б' : ['б', '6', 'b'],
  'в' : ['в', 'b', 'v'],
  'г' : ['г', 'r', 'g'],
  'д' : ['д', 'd', 'g'],
  'е' : ['е', 'e'],
  'ё' : ['ё', 'e'],
  'ж' : ['ж', 'zh', '*'],
  'з' : ['з', '3', 'z'],
  'и' : ['и', 'u', 'i'],
  'й' : ['й', 'u', 'i'],
  'к' : ['к', 'k', 'i{', '|{'],
  'л' : ['л', 'l', 'ji'],
  'м' : ['м', 'm'],
  'н' : ['н', 'h', 'n'],
  'о' : ['о', 'o', '0'],
  'п' : ['п', 'n', 'p'],
  'р' : ['р', 'r', 'p'],
  'с' : ['с', 'c', 's'],
  'т' : ['т', 'm', 't'],
  'у' : ['у', 'y', 'u'],
  'ф' : ['ф', 'f'],
  'х' : ['х', 'x', 'h', '}{'],
  'ц' : ['ц', 'c', 'u,'],
  'ч' : ['ч', 'ch'],
  'ш' : ['ш', 'sh'],
  'щ' : ['щ', 'sch'],
  'ь' : ['ь', 'b'],
  'ы' : ['ы', 'bi'],
  'ъ' : ['ъ'],
  'э' : ['э', 'e'],
  'ю' : ['ю', 'io'],
  'я' : ['я', 'ya'],
  ' ' : [' ']
        }

    async def __levenshtein_distance(self, offencive: str, word: str):
        m = len(offencive)
        n = len(word)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if offencive[i - 1] == word[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[m][n]
    async def check_message_for_violations(self, message: disnake.Message, model: Model):
        if model == Model.OFFENSES:
            text = message.content.lower()
            for key, value in self.__placeholder.items():
                for letter in value:
                    for txt_letter in text:
                        if txt_letter == letter:
                            text = text.replace(txt_letter, key)
            else:
                words = text.split()
                for word in words:
                    for off in self.offensive_expressions:
                            ld = await self.__levenshtein_distance(off, word)
                            if ld <= 1:
                                return True
                return False
        if model == Model.NSFW:
            structured = att_man.get_structured_message_attachments(message)
            for att_dict in structured:
                ...
            #todo: Написать логику работы проверки сообщения на нарушения
            return False # заглушка




