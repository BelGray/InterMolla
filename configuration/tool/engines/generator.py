import datetime

import sqlalchemy as db
import main
from configuration.database.db_req import *
class GlobalChatEmbedGenerator:

    __bot = main.client

    @staticmethod
    async def mention(user_id: int):
        return f"<@{user_id}>"

    @staticmethod
    async def create_request_body(name: str, avatar_url: str, badge_body: str, message: str, guild_name: str, color: str, guild_avatar_url: str, attachment: str, reference_message: str = None, reference_author_id: int = None) -> dict:
        int_color = int(color, 16)
        if reference_author_id is not None:
            ref_author = await GlobalChatEmbedGenerator.__bot.fetch_user(reference_author_id)
            ref_author_badge = connection.execute(db.select([tables.badges.columns.body]).where(tables.badges.columns.id == int((connection.execute(db.select([tables.users.columns.current_badge]).where(tables.users.columns.discord_id == str(reference_author_id))))[0])))
            ref_name = f"Ответ {ref_author.name} {ref_author_badge[0]}"
        else:
            ref_name = "0tвеt Atom#0000 ???"
        content = await GlobalChatEmbedGenerator.mention(reference_author_id) if reference_author_id is not None else ""
        reference_field = [] if reference_message is None or reference_author_id is None else [{
            'name': ref_name,
            'value': reference_message,
            'inline': False
        }]
        request_body = {
            'content': content,
            'embeds': [
                {
                    'title': f"{name} {badge_body}",
                    'description': message,
                    'fields': reference_field,
                    'image': {
                        'url': attachment
                    },
                    'thumbnail': {
                        'url': avatar_url
                    },
                    'color': int_color,
                    'timestamp': (datetime.datetime.now()).isoformat(),
                    'footer': {
                        'text': guild_name,
                        'icon_url': guild_avatar_url
                    }
                }
            ]
        }
        log.i('create_request_body', f'created message request body:\n{request_body}')
        return request_body
