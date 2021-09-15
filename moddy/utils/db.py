
from motor.motor_asyncio import AsyncIOMotorCollection


async def get_doc(coll: AsyncIOMotorCollection, filt: dict):
    pipeline = [{"match": filt}, {"$sample": {"size": 1}}]
    return [doc async for doc in coll.aggregate(pipeline)][0]


async def get_random_doc(coll: AsyncIOMotorCollection):
    pipeline = [{"$sample": {"size": 1}}]
    return [doc async for doc in coll.aggregate(pipeline)][0]
