import pika
import sys
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 连接消息队列服务器
#credentials = pika.PlainCredentials("hust", "hust")
#connection = pika.BlockingConnection(pika.ConnectionParameters(
#    host='222.20.79.153', port=5679, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='log',
                         exchange_type='topic')


def callback(ch, method, properties, body):
    # print(" [x] %r:%r" % (method.routing_key, body))
    print(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)



# queue_name = "logQue"
# result = channel.queue_declare(queue=queue_name, exclusive=True)
for i in range(1,11):
    binding_key = "thread-%s" % i
    queue_name = "thread-%s" % i

    result = channel.queue_declare(queue=queue_name, exclusive=False)
#queue_name = result.method.queue
#queue_name = "hello1"
# print(queue_name)


    channel.queue_bind(exchange='log',
                   queue=queue_name,
                    routing_key=binding_key)

#print(' [*] Waiting for logs. To exit press CTRL+C')



    channel.basic_consume(queue_name,
                        callback,
                        False)

channel.start_consuming()