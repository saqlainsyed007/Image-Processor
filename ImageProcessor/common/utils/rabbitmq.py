import pika
from django.conf import settings


class RabbitMQUtil:
    
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBIT_MQ_HOST, port=settings.RABBIT_MQ_PORT
            )
        )
        self.channel = self.connection.channel()

    def send_topic_message(self, exchange_name, topic_name, message, close_connection=True):
        self.channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
        self.channel.basic_publish(exchange=exchange_name, routing_key=topic_name, body=message)
        if close_connection:
            self.connection.close()
