from flask import Flask
from pyrogram import Client, enums, filters
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from datetime import datetime
from binascii import Error
import traceback

from configs import Config
from handlers.database import db
from handlers.add_user_to_db import add_user_to_database
from handlers.send_file import send_media_and_reply
from handlers.helpers import b64_to_str, str_to_b64
from handlers.check_user_status import handle_user_status
from handlers.force_sub_handler import handle_force_sub
from handlers.broadcast_handlers import main_broadcast_handler
from handlers.save_media import save_media_in_channel, save_batch_media_in_channel

MediaList = {}

Bot = Client(
    name=Config.BOT_USERNAME,
    in_memory=True,
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

async def is_premium_member(user_id):
    try:
        premium_users = await db.get_premium_users()
        return user_id in premium_users
    except Exception as e:
        print(f"Error checking premium status: {e}")
        return False

@Bot.on_message(filters.private)
async def handle_user(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)

@Bot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, cmd: Message):
    if cmd.from_user.id in Config.BANNED_USERS:
        await cmd.reply_text("Sorry, You are banned.")
        return

    if Config.UPDATES_CHANNEL:
        back = await handle_force_sub(bot, cmd)
        if back == 400:
            return

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await cmd.reply_text(f"Hi, I am back! Current date and time: {current_time}")

    usr_cmd = cmd.text.split("_", 1)[-1]
    if usr_cmd == "/start":
        await add_user_to_database(bot, cmd)
        await cmd.reply_text(
            Config.HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Updates Channel", url="https://t.me/netfilixmo_ch"),
                        InlineKeyboardButton("Search Movie", url="https://t.me/n_flixmovie")
                    ]
                ]
            )
        )
    else:
        try:
            try:
                file_id = int(b64_to_str(usr_cmd).split("_")[-1])
            except (Error, UnicodeDecodeError):
                file_id = int(usr_cmd.split("_")[-1])
            GetMessage = await bot.get_messages(chat_id=Config.DB_CHANNEL, message_ids=file_id)
            message_ids = []
            if GetMessage.text:
                message_ids = GetMessage.text.split(" ")
                await cmd.reply_text(
                    text=f"**Total Files:** `{len(message_ids)}`",
                    quote=True,
                    disable_web_page_preview=True
                )
            else:
                message_ids.append(int(GetMessage.id))
            for msg_id in message_ids:
                if await is_premium_member(cmd.from_user.id):
                    await send_media_and_reply(bot, user_id=cmd.from_user.id, file_id=msg_id)
                else:
                    await cmd.reply_text("This is a premium feature. Please subscribe to use this feature.")
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")

@Bot.on_message((filters.document | filters.video | filters.audio | filters.photo) & ~filters.chat(Config.DB_CHANNEL))
async def handle_media(bot: Client, message: Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        await add_user_to_database(bot, message)

        if Config.UPDATES_CHANNEL:
            back = await handle_force_sub(bot, message)
            if back == 400:
                return

        if message.from_user.id in Config.BANNED_USERS:
            await message.reply_text("Sorry, You are banned!\n\nContact [𝙎𝙪𝙥𝙥𝙤𝙧𝙩 𝙂𝙧𝙤𝙪𝙥](https://t.me/Netfilix_movie_shaport)",
                                     disable_web_page_preview=True)
            return

        if not Config.OTHER_USERS_CAN_SAVE_FILE:
            return

        await message.reply_text(
            text="**Choose an option from below:**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Save in Batch", callback_data="addToBatchTrue")],
                [InlineKeyboardButton("Get Sharable Link", callback_data="addToBatchFalse")]
            ]),
            quote=True,
            disable_web_page_preview=True
        )
    elif message.chat.type == enums.ChatType.CHANNEL:
        if (message.chat.id == int(Config.LOG_CHANNEL)) or (message.chat.id == int(Config.UPDATES_CHANNEL)) or message.forward_from_chat or message.forward_from:
            return
        elif int(message.chat.id) in Config.BANNED_CHAT_IDS:
            await bot.leave_chat(message.chat.id)
            return
        else:
            pass

        try:
            forwarded_msg = await message.forward(Config.DB_CHANNEL)
            file_er_id = str(forwarded_msg.id)
            share_link = f"https://t.me/{Config.BOT_USERNAME}?start=VJBotz_{str_to_b64(file_er_id)}"
            CH_edit = await bot.edit_message_reply_markup(message.chat.id, message.id,
                                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                                              "Get Sharable Link", url=share_link)]]))
            if message.chat.username:
                await forwarded_msg.reply_text(
                    f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/{message.chat.username}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
            else:
                private_ch = str(message.chat.id)[4:]
                await forwarded_msg.reply_text(
                    f"#CHANNEL_BUTTON:\n\n[{message.chat.title}](https://t.me/c/{private_ch}/{CH_edit.id}) Channel's Broadcasted File's Button Added!")
        except FloodWait as sl:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#FloodWait:\nGot FloodWait"

