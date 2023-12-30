from enum import Enum
from typing import Tuple, List, Any

import sqlalchemy as db
from configuration.database.sql_config import tables
from configuration.database.db_req import *


class EntType(Enum):
    USER = ('user', tables.users)
    GUILD = ('guild', tables.guilds)
    DONATE = ('donate', tables.donates)
    BADGE = ('badge', tables.badges)
    PROMO = ('promo', tables.promo)


class DiscordType(Enum):
    USER = ('user', tables.users)
    GUILD = ('guild', tables.guilds)


def exists(type: EntType, id: int) -> tuple[bool, list[Any]]:
        query_select = connection.execute(
            db.select(type.value[1]).where(type.value[1].columns.id.like(id))
        )
        res = query_select.fetchone()
        if res is None:
            log.e(f'exists ({type.value[0]})', f'Object not found [id: {id}]. Query result: {res}')
            return False, []
        log.s(f'exists ({type.value[0]})', f'Object found [id: {id}]. Query result: {res}')
        return True, list(res)


def is_registered(type: DiscordType, discord_id: int) -> tuple[bool, list[Any]]:
    query_select = connection.execute(
        db.select(type.value[1]).where(type.value[1].columns.discord_id.like(discord_id))
    )
    res = query_select.fetchone()
    if res is None:
        log.e(f'is_registered ({type.value[0]})', f'Object not found [discord_id: {discord_id}]. Query result: {res}')
        return False, []
    log.s(f'is_registered ({type.value[0]})', f'Object found [discord_id: {discord_id}]. Query result: {res}')
    return True, list(res)
