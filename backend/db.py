import os
from motor.motor_asyncio import AsyncIOMotorClient

_client: AsyncIOMotorClient | None = None


def get_db():
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    return _client[os.environ["DB_NAME"]]


async def ensure_indexes():
    db = get_db()
    await db.users.create_index("email", unique=True)
    await db.user_sessions.create_index("session_token")
    await db.user_sessions.create_index("expires_at", expireAfterSeconds=0)
    await db.login_attempts.create_index("identifier")
    await db.password_reset_tokens.create_index("expires_at", expireAfterSeconds=0)
    await db.daily_tasks.create_index([("user_id", 1), ("scheduled_date", 1)])
    await db.daily_tasks.create_index([("challenge_id", 1), ("day_number", 1)])
    await db.checkins.create_index([("user_id", 1), ("checkin_date", 1)], unique=True)
    await db.daily_bonuses.create_index(
        [("user_id", 1), ("bonus_date", 1), ("kind", 1)], unique=True)
    await db.point_transactions.create_index([("user_id", 1), ("created_at", -1)])
    await db.coach_messages.create_index([("user_id", 1), ("created_at", 1)])
