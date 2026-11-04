from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import events_crud
from app.api.models import EventDB, EventSchema

router = APIRouter()


@router.post("/", response_model=EventDB, status_code=201)
async def create_event(payload: EventSchema):
    event_id = await events_crud.post(payload)
    return {"id": event_id, **payload.dict()}


@router.get("/{id}/", response_model=EventDB)
async def read_event(id: int = Path(..., gt=0)):
    event = await events_crud.get(id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get("/", response_model=List[EventDB])
async def read_all_events():
    return await events_crud.get_all()


@router.put("/{id}/", response_model=EventDB)
async def update_event(payload: EventSchema, id: int = Path(..., gt=0)):
    event = await events_crud.get(id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event_id = await events_crud.put(id, payload)
    return {"id": event_id, **payload.dict()}


@router.delete("/{id}/", response_model=EventDB)
async def delete_event(id: int = Path(..., gt=0)):
    event = await events_crud.get(id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    await events_crud.delete(id)
    return event
