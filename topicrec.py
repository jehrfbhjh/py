import pika
import sys

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')
result = channel.queue_declare(exclusive=True,queue="l")
queue_name = result.method.queue
binding_keys = sys.argv[1:]
print(binding_keys)
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    #sys.exit(1)
for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key="#")
print(' [*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(queue_name,
                      callback,
                      False)
channel.start_consuming()