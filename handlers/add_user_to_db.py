from configs import Config
from handlers.database import db
from pyrogram import Client
from pyrogram.types import Message

async def add_user_to_database(bot: Client, cmd: Message):
    try:
        if not await db.is_user_exist(cmd.from_user.id):
            await db.add_user(cmd.from_user.id)
            
            if Config.LOG_CHANNEL:
                try:
                    await bot.send_message(
                        int(Config.LOG_CHANNEL),
                        f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
                    )
                except Exception as e:
                    print(f"Failed to send message to log channel: {e}")
    except Exception as e:
        print(f"Error in add_user_to_database: {e}")
