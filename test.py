#coding=utf-8
import pika

# connection 一个TCP的连接、
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

#  channel 是建立在TCP连接中的一个虚拟连接
channel = connection.channel()

# 声明一个queue
channel.queue_declare(queue='hello2')
# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='hello1',
                      body='2019-10-30 -- 2019-10-30',)
print(" [x] Sent" )
connection.close()




















