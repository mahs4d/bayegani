from bayegani.core.event import Event
from bayegani.worker.base import SyncWorker


class LocalWorker(SyncWorker):
    def _handler(self, event: Event):
        self.sink.save_events(events=[event])

    def start(self):
        self.source.add_handler(self._handler)
        self.source.consume_events()
