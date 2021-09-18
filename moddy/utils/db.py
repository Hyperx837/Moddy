from motor.motor_asyncio import AsyncIOMotorCollection


async def get_doc(coll: AsyncIOMotorCollection, filt: dict):
    pipeline = [{"$match": filt}, {"$sample": {"size": 1}}]
    try:
        return [doc async for doc in coll.aggregate(pipeline)][0]

    except IndexError:
        return None


async def get_random_doc(coll: AsyncIOMotorCollection):
    return await get_doc(coll, {})
