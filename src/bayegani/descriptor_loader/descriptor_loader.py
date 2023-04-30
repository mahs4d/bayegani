import importlib
from functools import lru_cache

from pydantic import BaseModel, Field

from bayegani.event_sink.base import SyncEventSink
from bayegani.event_source.base import SyncEventSource
from bayegani.worker.base import SyncWorker


class SourceDescriptor(BaseModel):
    cls: str = Field(..., alias='class')
    slug: str
    config: dict = {}


class SinkDescriptor(BaseModel):
    cls: str = Field(..., alias='class')
    slug: str
    config: dict = {}


class WorkerDescriptor(BaseModel):
    cls: str = Field(..., alias='class')
    config: dict = {}


class Descriptor(BaseModel):
    source: SourceDescriptor
    sink: SinkDescriptor
    worker: WorkerDescriptor


class DescriptorLoader:
    def __init__(self, descriptor: Descriptor):
        self.descriptor = descriptor

    @staticmethod
    def import_by_full_or_partial_name(
            cls: str,
            internal_package_name: str,
    ):
        split_name = cls.split('.')

        if len(split_name) == 1:
            return getattr(
                importlib.import_module(f'bayegani.{internal_package_name}'),
                cls,
            )

        return getattr(
            importlib.import_module('.'.join(split_name[:-1])),
            split_name[-1],
        )

    @lru_cache
    def get_event_source(self) -> SyncEventSource:
        cls_address = self.import_by_full_or_partial_name(
            cls=self.descriptor.source.cls,
            internal_package_name='event_source',
        )
        return cls_address(
            slug=self.descriptor.source.slug,
            config=self.descriptor.source.config,
        )

    @lru_cache
    def get_event_sink(self) -> SyncEventSink:
        cls_address = self.import_by_full_or_partial_name(
            cls=self.descriptor.sink.cls,
            internal_package_name='event_sink',
        )
        return cls_address(
            slug=self.descriptor.sink.slug,
            config=self.descriptor.sink.config,
        )

    @lru_cache
    def get_worker(self) -> SyncWorker:
        cls_address = self.import_by_full_or_partial_name(
            cls=self.descriptor.worker.cls,
            internal_package_name='worker',
        )
        return cls_address(
            source=self.get_event_source(),
            sink=self.get_event_sink(),
            config=self.descriptor.worker.config,
        )
