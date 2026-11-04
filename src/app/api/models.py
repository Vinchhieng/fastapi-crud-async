from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class NoteDB(NoteSchema):
    id: int


class EventSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=80)
    city: str = Field(..., min_length=2, max_length=50)
    price_usd: float = Field(..., ge=0)
    seats_left: int = Field(..., ge=0)


class EventDB(EventSchema):
    id: int
