from moddy.config import DB_NAME, MONGO_URL
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from moddy.utils import event_loop, console
from moddy.database.models import QuizModel
import pymongo

try:
    client = AsyncIOMotorClient(MONGO_URL, io_loop=event_loop)

except pymongo.errors.ServerSelectionTimeoutError:
    console.log(
        "[bold red]Database Error: Connection time out. start or restart mongod.service"
    )
database: AsyncIOMotorDatabase = client[DB_NAME]
