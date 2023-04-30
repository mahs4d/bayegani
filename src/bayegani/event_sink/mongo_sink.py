from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from bayegani.core.event import Event
from bayegani.event_sink.base import SyncEventSink


class Config(BaseModel):
    host: str
    port: int = 27017
    username: str
    password: str
    database: str
    collection: str


class MongoEventSink(SyncEventSink):
    def __init__(self, slug: str, config: dict):
        super().__init__(slug=slug, config=config)
        self.config = Config.parse_obj(config)

        self._client: MongoClient
        self._db: Database
        self._collection: Collection

    def setup(self):
        self._client = MongoClient(
            f'mongodb://{self.config.username}:{self.config.password}@{self.config.host}:{self.config.port}/'
        )
        self._db = self._client[self.config.database]
        self._collection = self._client[self.config.database][self.config.collection]

    def save_events(self, events: list[Event]):
        self._collection.insert_many([event.dict() for event in events])

    def teardown(self):
        self._client.close()
