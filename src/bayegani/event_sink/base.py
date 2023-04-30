from abc import ABC, abstractmethod

from bayegani.core.event import Event


class SyncEventSink(ABC):
    def __init__(self, slug: str, config: dict):
        self.slug = slug
        self.config = config
        self.handlers = set()

    @abstractmethod
    def setup(self):
        """
        Setup will be called once for all sinks before calling save or load.
        """

    @abstractmethod
    def save_events(self, events: list[Event]):
        """
        Save events to the sink.
        """

    @abstractmethod
    def teardown(self):
        """
        Teardown will happen at the end of application lifetime.
        """
