# _*_coding:utf-8_*_
import pika

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs',
                         exchange_type='topic')

result = channel.queue_declare(queue='thread-5')
#queue_name = result.method.queue
# 订阅：将消费者自己的queue绑定到交换机上
channel.queue_bind(exchange='logs',
                   queue='thread-5')
print(' [*] Waiting for logs. To exit press CTRL+C')
# 广播时：听众处理完消息后，不需要发送确认标志，无意义
channel.basic_consume('thread-5',
                      callback,
                      False)
channel.start_consuming()