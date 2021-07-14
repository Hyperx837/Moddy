from moddy.config import DB_NAME, MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from moddy.utils import event_loop
from moddy.database.models import QuizModel

client = AsyncIOMotorClient(MONGO_URL, io_loop=event_loop)
database: AsyncIOMotorDatabase = client[DB_NAME]
