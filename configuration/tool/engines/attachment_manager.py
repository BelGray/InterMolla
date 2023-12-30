import enum
import io
import os
import random
import disnake
import main
from configuration.tool.logger import log
from configuration.tool.config_manager import Admin
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class MediaFormat(enum.Enum):
    GIF = ['.gif']
    VIDEO = ['.mp4', '.webm', '.mov', '.wmv', '.mpeg', '.mpg']
    PICTURE = ['.jpg', '.png', '.jpeg', '.tiff', '.bmp', '.eps', '.svg', '.webp', '.heic', '.hdr', '.dng']
    NONE = []
    ALL = GIF.value + VIDEO.value + PICTURE.value

class AttachmentManager:

    def __init__(self):
        pass

    async def get_structured_message_attachments(self, message: disnake.Message) -> list:
        returning_body = []
        if message.attachments:
            for att in message.attachments:
                filename, ext = os.path.splitext(att.filename)
                returning_body.append({
                    'attachment': att,
                    'filename': filename,
                    'ext': ext,
                    'format': await self.__attachment_format(ext)
                })
        return returning_body

    async def __attachment_format(self, ext: str) -> MediaFormat:
        if ext in MediaFormat.PICTURE.value:
            return MediaFormat.PICTURE
        if ext in MediaFormat.VIDEO.value:
            return MediaFormat.VIDEO
        if ext in MediaFormat.GIF.value:
            return MediaFormat.GIF
        return MediaFormat.NONE

    async def save_img(self, attachment: disnake.Attachment) -> str:
        form = (attachment.filename.split('.'))[-1]
        name = os.path.splitext(attachment.filename)[0]
        if form in MediaFormat.PICTURE.value:
            unique_value = random.randint(100000000, 999999999)
            if not os.path.exists("attachments"):
                os.makedirs("attachments")
            await attachment.save("attachments/" + name + str(unique_value) + form)
            log.s('save_img', f'Saved new file named {name + str(unique_value) + form}')
            return name + str(unique_value) + form
        log.e('save_img', f'This attachment is not a picture')

    async def send_img(self, att: disnake.Attachment) -> disnake.Attachment:
        imgn = att.filename
        img = io.BytesIO(await att.read())
        channel_db = main.client.get_channel((Admin.channels())['attachments'])
        att = await channel_db.send(file=disnake.File(img, imgn))
        log.i('send_img', f'Image has been sent to the attachments channel. Attachment url: {att.attachments[0].url}')
        return att.attachments[0]

    async def send_img_from_path(self, unique_filename: str) -> disnake.Attachment:
        with open('attachments/' + unique_filename, 'rb') as f:
            read_file = io.BytesIO(f.read())
        channel_db = main.client.get_channel((Admin.channels())['attachments'])
        att = await channel_db.send(file=disnake.File(read_file, unique_filename))
        log.i(f'send_img_from_path. unique_filename: {unique_filename}', f'Image has been sent to the attachments channel. Attachment url: {att.attachments[0].url}')
        return att.attachments[0]

    async def send_not_available_img(self, att: disnake.Attachment) -> disnake.Attachment:
        imgn = att.filename
        img = Image.open(io.BytesIO(await att.read())).filter(ImageFilter.GaussianBlur(radius=30))
        draw = ImageDraw.Draw(img)
        text = "InterMolla doesn’t support pictures now"
        font = ImageFont.truetype("fonts/arial_bold.ttf", size=30)
        text_width, text_height = draw.textsize(text, font=font)
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        channel_db = main.client.get_channel((Admin.channels())['attachments'])
        att = await channel_db.send(file=disnake.File(img.tobytes(), imgn))
        log.i('send_not_available_img', f'Image has been sent to the attachments channel. Attachment url: {att.attachments[0].url}')
        return att.attachments[0]

    async def remove_img(self, unique_filename: str):
        fn = 'attachments/' + unique_filename
        if os.path.exists(fn):
            os.remove(fn)
            log.s('remove_img', f'"{fn}" has been removed')
            return
        log.e('remove_img', f'There is no file named "{fn}"')

