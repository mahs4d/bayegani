from abc import ABC, abstractmethod
from typing import Callable

from bayegani.core.event import Event


class SyncEventSource(ABC):
    def __init__(self, slug: str, config: dict):
        self.slug = slug
        self.config = config
        self.handlers = set()

    @abstractmethod
    def setup(self):
        """
        Setup will be called for all sources before calling consume or publish on any of them.
        """

    def add_handler(self, handler: Callable[[Event], None]):
        """
        Add a handler to be called once an event is received.
        """
        self.handlers.add(handler)

    @abstractmethod
    def consume_events(self):
        """
        Start consuming events and calling handlers.
        """

    @abstractmethod
    def teardown(self):
        """
        Teardown will happen at the end of application lifetime.
        """
