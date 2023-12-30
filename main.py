# -*- coding: utf-8 -*-
from bot_commands import enable_global
from configuration.tool.config_manager import *
from configuration.tool.engines.sender import *
from configuration.tool.themes import *
import disnake
from disnake.ext import commands
from configuration.database.db_req import DatabaseTablesManager

theme = Themes.REGULAR.value # todo: исправить переменную темы
client = commands.Bot(command_prefix="?", case_insensitive=True, intents=disnake.Intents.all())
cd_mapping = commands.CooldownMapping.from_cooldown(1, 3, commands.BucketType.user)
botSystemColor = disnake.Color.red()
client.remove_command('help')
botversion = "beta"

ConfigManager.init_bot_config()
sender = GlobalChatSenderEngine(client)

@client.event
async def on_ready():
    log.s('on_ready', 'Connected to Discord API successfully')
    ConfigManager.get_api_token(Services.QIWI)
    await sender.set_update_active_guilds_loop(5, 1800)

@client.command()
async def load(ctx, extension):
    if Admin.user_is_trusted(ctx.author.id):
        if not os.path.exists('cogs'):
            os.mkdir('cogs')
            log.i('load', 'Created new dir "cogs"')
        client.load_extension(f'cogs.{extension}')
        log.s('load', 'Cogs are loaded')
    else:
        log.w('load', f'Access denied, that is why cogs are not loaded! Author id: {ctx.author.id}')

@client.command()
async def unload(ctx, extension):
    if Admin.user_is_trusted(ctx.author.id):
        if not os.path.exists('cogs'):
            os.mkdir('cogs')
            log.i('unload', 'Created new dir "cogs"')
        client.unload_extension(f'cogs.{extension}')
        log.s('unload', 'Cogs are unloaded')
    else:
        log.w('unload', f'Access denied, that is why cogs are not unloaded! Author id: {ctx.author.id}')

@client.command()
async def reload(ctx, extension):
    if Admin.user_is_trusted(ctx.author.id):
        if not os.path.exists('cogs'):
            os.mkdir('cogs')
            log.i('reload', 'Created new dir "cogs"')
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        log.s('reload', 'Cogs are reloaded')
    else:
        log.w('reload', f'Access denied, that is why cogs are not reloaded! Author id: {ctx.author.id}')

for fn in os.listdir('./cogs'):
    if fn.endswith('.py'):
        client.load_extension(f'cogs.{os.path.splitext(fn)}')

client.add_cog(enable_global.EnableGlobal(client))
try:
    client.run(ConfigManager.get_api_token(Services.DISCORD))
except Exception as e:
    ConfigManager.set_api_token(Services.DISCORD, None)
    raise e
