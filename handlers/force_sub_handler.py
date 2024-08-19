import asyncio
from typing import Union
from configs import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

async def get_invite_link(bot: Client, chat_id: Union[str, int]):
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=chat_id)
        return invite_link
    except FloodWait as e:
        print(f"Sleep of {e.value}s caused by FloodWait ...")
        await asyncio.sleep(e.value)
        return await get_invite_link(bot, chat_id)

async def handle_force_sub(bot: Client, cmd: Message):
    if Config.UPDATES_CHANNEL and Config.UPDATES_CHANNEL.startswith("-100"):
        channel_chat_id = int(Config.UPDATES_CHANNEL)
    elif Config.UPDATES_CHANNEL:
        channel_chat_id = Config.UPDATES_CHANNEL
    else:
        # Handle the error when the UPDATES_CHANNEL configuration is missing or invalid
        await cmd.reply("Updates channel is not configured properly. Please check the configuration.")
        return

    try:
        invite_link = await get_invite_link(bot, channel_chat_id)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=invite_link.invite_link)]
        ])
        await cmd.reply("Please join the channel to continue:", reply_markup=keyboard)
    except UserNotParticipant:
        # Handle case where the user is not a participant of the channel
        await cmd.reply("You are not a participant of the channel. Please join the channel to continue.")
    except FloodWait as e:
        # Handle FloodWait error if it occurs
        await asyncio.sleep(e.value)
        await handle_force_sub(bot, cmd)
    except Exception as e:
        # Handle any other exceptions
        await cmd.reply(f"An error occurred: {str(e)}")
