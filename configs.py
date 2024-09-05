import os

class Config(object):
    API_ID = int(os.environ.get("API_ID", "27002519"))
    API_HASH = os.environ.get("API_HASH", "1033ee721101d78366b4ac46aadf3930")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7389324956:AAEqLRq_y4Auia1s-l5e-O-8GRkw48yrTlM")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "Netflix_file_storebot")
    DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002244711970"))
    SHORTLINK_URL = os.environ.get('SHORTLINK_URL', "shortxlinks.com")
    SHORTLINK_API = os.environ.get('SHORTLINK_API', "fa2a0768fc8d2a51b22e46293634a52670a73c7a")
    BOT_OWNER = int(os.environ.get("BOT_OWNER", "6174868004"))
    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://hackinggm69:zV0SIntQrc8PXX3R@cluster0.sqzqvsg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "-1002233212878")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002192763590"))
    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
    FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", True))
    BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
    BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "").split()))
    OTHER_USERS_CAN_SAVE_FILE = bool(os.environ.get("OTHER_USERS_CAN_SAVE_FILE", True))
    RENAME_MODE = bool(os.environ.get('RENAME_MODE', False)) # Ensure this line is present
    BOT_VERSION = "1.0.0"
    
    ABOUT_BOT_TEXT = f"""
    ᴛʜɪs ɪs ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ ᴀᴘs_ғɪʟᴇsᴛᴏʀᴇ ʙᴏᴛ.
    sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴍᴇᴅɪᴀ ᴏʀ ғɪʟᴇ. ɪ ᴄᴀɴ ᴡᴏʀᴋ ɪɴ ᴄʜᴀɴɴᴇʟ ᴛᴏᴏ. ᴀᴅᴅ ᴍᴇ ᴛᴏ ᴄʜᴀɴɴᴇʟ ᴡɪᴛʜ ᴇᴅɪᴛ ᴘᴇʀᴍɪssɪᴏɴ, ɪ ᴡɪʟʟ sᴀᴠᴇ ᴜᴘʟᴏᴀᴅᴇᴅ ғɪʟᴇ ɪɴ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ sʜᴀʀᴇ ᴀ sʜᴀʀᴇᴀʙʟᴇ ʟɪɴᴋ.
    ╭────[ 🔅FɪʟᴇSᴛᴏʀᴇBᴏᴛ🔅]────⍟
    │
    ├🔸 My Name: [FileStore Bot](https://t.me/{BOT_USERNAME})
    │
    ├🔸 Language: [Python 3](https://www.python.org)
    │
    ├🔹 Library: [Pyrogram](https://docs.pyrogram.org)
    │
    ╰──────[ 😎 ]───────────⍟
    """
    ABOUT_DEV_TEXT = f"""
    🧑🏻‍💻 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿: [R3](https://telegram.me/Rajps33)

    I am Super noob Please Support My Hard Work.

    [Donate Me](https://t.me/Rajps33)
    """
    HOME_TEXT = """
    Hᴇʟʟᴏ, [{}](tg://user?id={})\n\nᴛʜɪs ɪs ᴀ ᴘᴇʀᴍᴀɴᴇɴᴛ  **ғɪʟᴇsᴛᴏʀᴇ ʙᴏᴛ**.
    ʜᴏᴡ ᴛᴏ ᴜsᴇ ʙᴏᴛ & ɪᴛ's ʙᴇɴᴇғɪᴛs ??

    📢 sᴇɴᴅ ᴍᴇ ᴀɴʏ ғɪʟᴇ & ɪᴛ ᴡɪʟʟ ʙᴇ ᴜᴘʟᴏᴀᴅᴇᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ & ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇ ʟɪɴᴋ.

    ⚠️ ʙᴇɴᴇғɪᴛs: ɪғ ʏᴏᴜ ʜᴀᴠᴇ ᴀ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴏᴠɪᴇ ᴄʜᴀɴɴᴇʟ ᴏʀ ᴀɴʏ ᴄᴏᴘʏʀɪɢʜᴛ ᴄʜᴀɴɴᴇʟ, ᴛʜᴇɴ ɪᴛs ᴜsᴇғᴜʟ ғᴏʀ ᴅᴀɪʟʏ ᴜsᴀɢᴇ, ʏᴏᴜ ᴄᴀɴ sᴇɴᴅ ᴍᴇ ʏᴏᴜʀ ғɪʟᴇ & ɪ ᴡɪʟʟ sᴇɴᴅ ᴘᴇʀᴍᴀɴᴇɴᴛ ʟɪɴᴋ ᴛᴏ ʏᴏᴜ & ᴄʜᴀɴɴᴇʟ ᴡɪʟʟ ʙᴇ sᴀғᴇ ғʀᴏᴍ ᴄᴏᴘʏʀɪɢʜᴛ ɪɴғʀɪɢᴍᴇɴᴛ ɪssᴜᴇ. ɪ sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ ᴀʟsᴏ ʏᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ᴀʙᴏᴜᴛ ʙᴏᴛ.

    ❌ ᴘᴏʀɴᴏɢʀᴀᴘʜʏ ᴄᴏɴᴛᴇɴᴛs ᴀʀᴇ sᴛʀɪᴄᴛʟʏ ᴘʀᴏʜɪʙɪᴛᴇᴅ & ɢᴇᴛ ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ.
    """
