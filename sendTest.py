#coding=utf-8
import pika
import time
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 连接消息队列服务器
#credentials = pika.PlainCredentials("guest", "guest")
#connection = pika.BlockingConnection(pika.ConnectionParameters(
#    host='localhost', port=5679, credentials=credentials))

#  channel 是建立在TCP连接中的一个虚拟连接
channel = connection.channel()

# 声明一个queue
channel.queue_declare(queue='hello')

for i in range(10):
    # n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
    print("Sent a Message...")
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='2019-10-30 -- 2020-10-30 --' +"%s" %i,)
    time.sleep(1)

#connection.close()



#对应线程接收log日志
#for i in range(10):
    #channel = connection.channel()


    # channel.queue_declare(queue='hello6')

def callback(ch, method, properties, body, ):
    print(body.decode())

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume('Thread-'+"%s" %8, callback, auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()





















