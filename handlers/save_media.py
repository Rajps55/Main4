import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config
from handlers.helpers import str_to_b64

async def save_media_in_channel(bot: Client, message: Message):
    try:
        if Config.SAVE_MEDIA_AS_COPY:
            return await bot.copy_message(
                chat_id=Config.DB_CHANNEL,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        else:
            return await bot.forward_messages(
                chat_id=Config.DB_CHANNEL,
                from_chat_id=message.chat.id,
                message_ids=message.message_id
            )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await save_media_in_channel(bot, message)

async def save_batch_media_in_channel(bot: Client, messages: list):
    for message in messages:
        try:
            if Config.SAVE_MEDIA_AS_COPY:
                await bot.copy_message(
                    chat_id=Config.DB_CHANNEL,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id
                )
            else:
                await bot.forward_messages(
                    chat_id=Config.DB_CHANNEL,
                    from_chat_id=message.chat.id,
                    message_ids=message.message_id
                )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await save_batch_media_in_channel(bot, messages)
