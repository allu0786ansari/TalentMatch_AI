import pika
import json
from typing import Any, Callable
from ..config import settings

class MessageQueue:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(settings.RABBITMQ_URL)
        )
        self.channel = self.connection.channel()
        
    def setup_queue(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name, durable=True)
        
    def publish_message(self, queue_name: str, message: Any):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        
    def consume_messages(self, queue_name: str, callback: Callable):
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )
        self.channel.start_consuming()
        
    def close(self):
        self.connection.close()