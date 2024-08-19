import time
import string
import random
import datetime
import aiofiles
import asyncio
import traceback
import aiofiles.os
from configs import Config
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    UserIsBlocked,
    PeerIdInvalid
)

broadcast_ids = {}

async def send_msg(user_id, message):
    try:
        if Config.BROADCAST_AS_COPY:
            await message.copy(chat_id=user_id)
        else:
            await message.forward(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

async def main_broadcast_handler(m, db):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for _ in range(3)])
        if broadcast_id not in broadcast_ids:
            break
    out = await m.reply_text(
        text="Broadcast Started! You will be notified with log file when all the users are notified."
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = {
        'total': total_users,
        'current': done,
        'failed': failed,
        'success': success
    }
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(
                user_id=int(user['id']),
                message=broadcast_msg
            )
            if msg:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            elif sts == 400:
                await db.delete_user(user['id'])
                failed += 1
            done += 1
            broadcast_ids[broadcast_id].update(
                dict(
                    current=done,
                    failed=failed,
                    success=success
                )
            )
            if broadcast_id not in broadcast_ids:
                break
    if broadcast_id in broadcast_ids:
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    summary_text = (
        f"broadcast completed in `{completed_in}`\n\n"
        f"Total users {total_users}.\n"
        f"Total done {done}, {success} success and {failed} failed."
    )
    if failed == 0:
        await m.reply_text(text=summary_text, quote=True)
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=summary_text,
            quote=True
        )
    await aiofiles.os.remove('broadcast.txt')
