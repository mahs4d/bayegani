import json
import time

import pika
import pika.channel
import pika.spec
from pydantic import BaseModel

from bayegani.core.event import Event, Metadata
from bayegani.event_source.base import SyncEventSource


class Binding(BaseModel):
    exchange: str
    routing_key: str


class Config(BaseModel):
    host: str
    port: int = 5672
    vhost: str = "/"
    username: str = "guest"
    password: str = "guest"
    queue_name: str
    bindings: list[Binding]
    prefetch_count: int = 100


class RabbitmqEventSource(SyncEventSource):
    def __init__(self, slug: str, config: dict):
        super().__init__(slug=slug, config=config)
        self.config = Config.parse_obj(config)

    def setup(self):
        self._connection = pika.BlockingConnection(
            parameters=pika.ConnectionParameters(
                host=self.config.host,
                port=self.config.port,
                virtual_host=self.config.vhost,
                credentials=pika.PlainCredentials(
                    username=self.config.username,
                    password=self.config.password,
                ),
            ),
        )

        self._channel = self._connection.channel()
        self._channel.basic_qos(
            prefetch_count=self.config.prefetch_count,
        )

        self._channel.queue_declare(
            queue=self.config.queue_name,
            auto_delete=True,
        )

        for binding in self.config.bindings:
            self._channel.queue_bind(
                queue=self.config.queue_name,
                exchange=binding.exchange,
                routing_key=binding.routing_key,
            )

    def _on_message_callback(
            self,
            ch: pika.channel.Channel,
            method_frame: pika.spec.Basic.Deliver,
            properties: pika.spec.BasicProperties,
            body: bytes,
    ):
        parent_id = properties.headers.get('parent_id')
        event = Event(
            source=self.slug,
            timestamp=time.time_ns() // 1_000_000,
            metadata=Metadata(
                event_id=properties.message_id,
                parent_id=parent_id,
                correlation_id=properties.correlation_id,
                original_timestamp=int(properties.timestamp) if properties.timestamp else None,
                type=properties.type,
                extra={
                    'exchange': method_frame.exchange,
                    'routing_key': method_frame.routing_key,
                },
            ),
            payload=json.loads(body.decode(encoding='utf-8')),
        )

        for handler in self.handlers:
            handler(event)

        ch.basic_ack(
            delivery_tag=method_frame.delivery_tag,
            multiple=False,
        )

    def consume_events(self):
        self._channel.basic_consume(
            queue=self.config.queue_name,
            on_message_callback=self._on_message_callback,
            auto_ack=False,
        )
        self._channel.start_consuming()

    def teardown(self):
        self._channel.stop_consuming()
        self._channel.close()
        self._connection.close()
