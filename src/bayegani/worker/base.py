from abc import ABC, abstractmethod

from bayegani.event_sink.base import SyncEventSink
from bayegani.event_source.base import SyncEventSource


class SyncWorker(ABC):
    def __init__(
            self,
            source: SyncEventSource,
            sink: SyncEventSink,
            config: dict,
    ):
        self.source = source
        self.sink = sink
        self.config = config

    def setup(self):
        self.source.setup()
        self.sink.setup()

    @abstractmethod
    def start(self):
        """
        Start storing source events into sink.
        """

    def teardown(self):
        self.source.teardown()
        self.sink.teardown()
