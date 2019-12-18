#coding=utf-8
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

#channel.queue_declare(queue='hello6')


def callback(ch, method, properties, body,):
    print(body.decode())


    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume('Thread-4', callback, auto_ack=False)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

