import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='log',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True,queue="")
queue_name = result.method.queue

binding_key = "#"

channel.queue_bind(exchange='log',
                   queue=queue_name,
                    routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue_name,
                      callback,
                      False)

channel.start_consuming()