import disnake
from disnake.ext import commands
from configuration.tool import logger
from configuration.tool.tools import *

class EnableGlobal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="enable_global",
        description="Подключить сервер к глобальному чату",
    )
    @commands.has_permissions(manage_channels=True)
    async def enable_global(self, inter: disnake.ApplicationCommandInteraction, channel: disnake.TextChannel):
        g_reg = is_registered(DiscordType.GUILD, inter.guild.id)
        if g_reg[0]:
            if g_reg[1][2] == "":
                ...
                #todo: Дописать команду включения глобального чата
            return
