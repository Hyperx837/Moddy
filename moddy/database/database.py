import pymongo
from moddy.database.models import QuizModel
from moddy.logger import logger
from moddy.utils.misc import event_loop, get_secret
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)

mongo_url = get_secret("common.mongo.url")
db_name = get_secret("db_name")

try:
    client = AsyncIOMotorClient(mongo_url, io_loop=event_loop)

except pymongo.errors.ServerSelectionTimeoutError:
    logger.error("Database Error: Connection time out. start or restart mongod.service")
database: AsyncIOMotorDatabase = client[db_name]
