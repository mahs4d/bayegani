from pydantic import BaseModel


class Metadata(BaseModel):
    event_id: str | None = None
    parent_id: str | None = None
    correlation_id: str | None = None
    original_timestamp: int | None = None
    type: str | None = None
    extra: dict = {}


class Tag(BaseModel):
    key: str
    value: str


class Event(BaseModel):
    source: str
    timestamp: int
    metadata: Metadata
    payload: dict
    tags: list[Tag] = []
