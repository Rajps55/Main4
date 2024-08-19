import datetime
import motor.motor_asyncio
from configs import Config

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )

    async def add_user(self, id):
        try:
            user = self.new_user(id)
            await self.col.insert_one(user)
        except Exception as e:
            print(f"Failed to add user {id}: {e}")

    async def is_user_exist(self, id):
        try:
            user = await self.col.find_one({'id': int(id)})
            return True if user else False
        except Exception as e:
            print(f"Failed to check user existence for {id}: {e}")
            return False

    async def total_users_count(self):
        try:
            count = await self.col.count_documents({})
            return count
        except Exception as e:
            print(f"Failed to count users: {e}")
            return 0

    async def get_all_users(self):
        try:
            all_users = self.col.find({})
            return all_users
        except Exception as e:
            print(f"Failed to retrieve all users: {e}")
            return []

    async def delete_user(self, user_id):
        try:
            await self.col.delete_many({'id': int(user_id)})
        except Exception as e:
            print(f"Failed to delete user {user_id}: {e}")

    async def remove_ban(self, id):
        try:
            ban_status = dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
            await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
        except Exception as e:
            print(f"Failed to remove ban for {id}: {e}")

    async def ban_user(self, user_id, ban_duration, ban_reason):
        try:
            ban_status = dict(
                is_banned=True,
                ban_duration=ban_duration,
                banned_on=datetime.date.today().isoformat(),
                ban_reason=ban_reason
            )
            await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})
        except Exception as e:
            print(f"Failed to ban user {user_id}: {e}")

    async def get_ban_status(self, id):
        try:
            default = dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
            user = await self.col.find_one({'id': int(id)})
            return user.get('ban_status', default)
        except Exception as e:
            print(f"Failed to get ban status for {id}: {e}")
            return default

    async def get_all_banned_users(self):
        try:
            banned_users = self.col.find({'ban_status.is_banned': True})
            return banned_users
        except Exception as e:
            print(f"Failed to retrieve banned users: {e}")
            return []

db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)
