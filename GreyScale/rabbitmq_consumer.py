import json
import os
import pika
import sys

from utils import convert_to_greyscale


def callback(ch, method, properties, body):
    print(f' [x] Received {body}')
    convert_to_greyscale(body)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='image-processor-rabbitmq'))
    channel = connection.channel()

    exchange_name = 'image_exchange'
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    topic_name = 'image.convert.greyscale'
    channel.queue_bind(
        exchange=exchange_name, queue=queue_name, routing_key=topic_name
    )

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True
    )

    print('Listner started waiting for images.')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
