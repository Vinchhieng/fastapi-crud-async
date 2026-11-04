from app.api.models import EventSchema
from app.db import events, database


async def post(payload: EventSchema):
    query = events.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get(id: int):
    query = events.select().where(events.c.id == id)
    return await database.fetch_one(query=query)


async def get_all():
    query = events.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: EventSchema):
    query = (
        events.update()
        .where(events.c.id == id)
        .values(**payload.dict())
        .returning(events.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = events.delete().where(events.c.id == id)
    return await database.execute(query=query)
