import asyncio
from typing import Union
from configs import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

async def get_invite_link(bot: Client, chat_id: Union[str, int], retries=5):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        if retries > 0:
            await asyncio.sleep(e.value)
            return await get_invite_link(bot, chat_id, retries=retries-1)
        else:
            print(f"Failed to get invite link after multiple retries: {e}")

async def handle_force_sub(bot: Client, cmd: Message):
    channel_chat_id = int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL

    try:
        invite_link = await get_invite_link(bot, channel_chat_id)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=invite_link.invite_link)]
        ])
        await cmd.reply("Please join the channel to continue:", reply_markup=keyboard)
    except UserNotParticipant:
        await cmd.reply("You are not a participant of the channel. Please join the channel to continue.")
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await handle_force_sub(bot, cmd)
    except Exception as e:
        await cmd.reply(f"An error occurred: {str(e)}")
