import pymongo
from moddy.config import DB_NAME, MONGO_URL
from moddy.database.models import QuizModel
from moddy.logger import logger
from moddy.utils import console, event_loop
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

try:
    client = AsyncIOMotorClient(MONGO_URL, io_loop=event_loop)

except pymongo.errors.ServerSelectionTimeoutError:
    logger.error("Database Error: Connection time out. start or restart mongod.service")
database: AsyncIOMotorDatabase = client[DB_NAME]
