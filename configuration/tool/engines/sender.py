import datetime
import sqlalchemy as db

from configuration.database.db_req import connection
from configuration.database.sql_config import *
from configuration.tool.logger import log
from configuration.tool.config_manager import ConfigManager, Services
import aiohttp
import asyncio
import disnake
from disnake.ext import commands


class GlobalChatSenderEngine:
    __api_base_url = "https://discord.com/api/v10/"

    def __init__(self, client: commands.Bot):
        self.__overload = 0
        self.__active_guilds = []
        self.__client = client
        self.__active_guilds_data = {}

    @property
    def active_guilds(self):
        return self.__active_guilds

    @active_guilds.setter
    def active_guilds(self, value):
        self.__active_guilds = value

    @property
    def active_guilds_data(self):
        return self.__active_guilds_data

    @active_guilds_data.setter
    def active_guilds_data(self, value):
        self.__active_guilds_data = value

    async def append_active_guild(self, guild_id: int):
      if guild_id not in self.__active_guilds and guild_id not in self.__active_guilds_data:
        self.__active_guilds_data[guild_id] = {
            'messages': 0,
            'last_update': int((datetime.datetime.now()).timestamp())
        }
        self.__active_guilds.append(guild_id)
        log.s('append_active_guild', f'Append new active guild with id: {guild_id}')
        return
      log.w('append_active_guild', f'Active guild with id {guild_id} already exists')

    async def remove_active_guild(self, guild_id: int):
        if guild_id in self.__active_guilds and guild_id in self.__active_guilds_data:
            del self.__active_guilds_data[guild_id]
            self.__active_guilds.remove(guild_id)
            log.s('remove_active_guild', f'Remove an active guild with id: {guild_id}')
            return
        log.w('remove_active_guild', f'Active guild with id {guild_id} does not exist')

    async def inflate_active_guilds(self):
        log.i('inflate_active_guilds', 'Inflated new active guilds list')
        bot = self.__client
        #active_guilds = [guild.id for guild in bot.guilds]
        self.__overload = 0
        for guild in bot.guilds:
            self.__active_guilds_data[guild.id] = {
                'messages': 0,
                'last_update': int((datetime.datetime.now()).timestamp())
            }
        self.__active_guilds = sorted(self.__active_guilds_data.keys(), key=lambda x: (self.__active_guilds_data[x]['messages'], self.__active_guilds_data[x]['last_update']), reverse=True)
        log.s('inflate_active_guilds', f'Successfully inflated active guilds.\n{self.__active_guilds}')

    async def update_active_guilds(self):
        self.__active_guilds = sorted(self.__active_guilds_data.keys(), key=lambda x: (self.__active_guilds_data[x]['messages'], self.__active_guilds_data[x]['last_update']), reverse=True)
        log.s('update_active_guilds', f'Updated active guilds list.\n{self.__active_guilds}')

    async def set_update_active_guilds_loop(self, every_seconds: float, reset_in_seconds: float):
        await self.inflate_active_guilds()
        reset_in = reset_in_seconds
        while True:
            await asyncio.sleep(every_seconds)
            reset_in -= every_seconds
            await self.update_active_guilds()
            if reset_in <= 0:
                await self.inflate_active_guilds()
                reset_in = reset_in_seconds
                continue

    async def detect_message(self, guild_id: int):
        if self.__active_guilds_data[guild_id] in self.__active_guilds_data:
            log.i('detect_message', f'Detected a message from guild with id {guild_id}.')
            self.__active_guilds_data[guild_id]['messages'] += 1
            self.__active_guilds_data[guild_id]['last_update'] = int((datetime.datetime.now()).timestamp())

    async def send(self, message_request_body: dict):
        token = ConfigManager.get_api_token(service=Services.DISCORD)
        current_list = self.active_guilds
        async with aiohttp.ClientSession() as session:
            async for guild_id in self.__get_each_active_guild(current_list):
                log.s('send', f'New guild cycle iteration. Current guild id: {guild_id}')
                channel = connection.execute(db.select([tables.guilds.columns.global_chat_channel_id, tables.guilds.columns.ban]).where(tables.guilds.columns.discord_id == str(guild_id)))
                if channel[0] != "" and channel[1] != 1:
                    await asyncio.sleep(self.__overload)
                    async with session.post(url=self.__api_base_url + f"channels/{channel[0]}/messages", data=message_request_body, headers={'Authorization': f'Bot {token}'}) as response:
                        status = response.status
                        while status == 429:
                            log.e('send', f'Discord API returned HTTP Status 429. Delayed guild id: {guild_id}')
                            await asyncio.sleep(self.__overload)
                            async with session.post(url=self.__api_base_url + f"channels/{channel[0]}/messages", data=message_request_body, headers={'Authorization': f'Bot {token}'}) as retry_response:
                                status = retry_response.status
                                log.i('send', f'Resend status: {status}')
                                if status == 429:
                                    self.__overload += 0.25
                                    log.w('send', f'The overload is equals to {self.__overload}')
                                else:
                                    log.s('send', f'Successfully sent. Guild id: {guild_id}')
                                    break
                else:
                    log.w('send', f'The guild with id {guild_id} has been refused.')

    async def __get_each_active_guild(self, guilds_list: list):
        for active_guild in guilds_list:
            yield active_guild
