import sqlalchemy as alch
from configuration.tool.logger import log

db_engine = alch.create_engine('sqlite:///inter_molla.db', echo=True)
connection = db_engine.connect()
meta = alch.MetaData()
class DatabaseTablesManager:

    def __init__(self):
        users, guilds, donates, badges, badge_body, promo, users_used_promo = self.__init_database()
        self.__users = users
        self.__guilds = guilds
        self.__donates = donates
        self.__badges = badges
        self.__badge_body = badge_body
        self.__promo = promo
        self.__users_used_promo = users_used_promo


    @property
    def users(self):
        return self.__users

    @property
    def guilds(self):
        return self.__guilds

    @property
    def donates(self):
        return self.__donates

    @property
    def badges(self):
        return self.__badges

    @property
    def badge_body(self):
        return self.__badge_body

    @property
    def promo(self):
        return self.__promo

    @property
    def users_used_promo(self):
        return self.__users_used_promo

    def __init_database(self):
        log.i('init_database', 'Init process started')
        users = alch.Table('users', meta,
            alch.Column('id', alch.INT, primary_key=True),
            alch.Column('discord_id', alch.VARCHAR),
            alch.Column('mollcoins', alch.BIGINT),
            alch.Column('current_badge', alch.INTEGER),
            alch.Column('premium', alch.BOOLEAN),
            alch.Column('bot_ban', alch.BOOLEAN),
            alch.Column('mentions', alch.BOOLEAN),
            alch.Column('links_perm', alch.BOOLEAN),
            alch.Column('display_avatar', alch.BOOLEAN),
            alch.Column('display_name', alch.BOOLEAN),
            alch.Column('display_guild', alch.BOOLEAN),
            alch.Column('color', alch.VARCHAR),
            alch.Column('custom_name', alch.VARCHAR),
            alch.Column('custom_avatar', alch.VARCHAR),
        )

        guilds = alch.Table('guilds', meta,
            alch.Column('id', alch.INT, primary_key=True),
            alch.Column('discord_id', alch.VARCHAR),
            alch.Column('global_chat_channel_id', alch.VARCHAR),
            alch.Column('ban', alch.BOOLEAN),
        )

        donates = alch.Table('donates', meta,
            alch.Column('id', alch.INT, primary_key=True),
            alch.Column('user_id', alch.BIGINT),
            alch.Column('amount', alch.BIGINT),
            alch.Column('date', alch.VARCHAR)
        )

        badges = alch.Table('badges', meta,
            alch.Column('id', alch.INT, primary_key=True),
            alch.Column('name', alch.VARCHAR),
            alch.Column('animated', alch.BOOLEAN),
            alch.Column('neon', alch.BOOLEAN),
            alch.Column('random', alch.BOOLEAN),
        )

        badge_body = alch.Table('badge_body', meta,
            alch.Column('badge_id', alch.INT),
            alch.Column('body', alch.VARCHAR)
        )

        promo = alch.Table('promo', meta,
            alch.Column('id', alch.INT, primary_key=True),
            alch.Column('body', alch.VARCHAR),
            alch.Column('description', alch.VARCHAR),
            alch.Column('usages', alch.INT),
            alch.Column('item_id', alch.INT)
        )

        users_used_promo = alch.Table('users_used_promo', meta,
            alch.Column('promo_id', alch.INT),
            alch.Column('user_id', alch.INT)
        )

        meta.create_all(db_engine)

        log.i("init_database", "Init process finished")

        return users, guilds, donates, badges, badge_body, promo, users_used_promo

