#coding=utf-8
import pika
import logging
from multiprocessing import Process
from python_logging_rabbitmq import RabbitMQHandler

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

rabbit = RabbitMQHandler(host='localhost', port=5672)
logger.addHandler(rabbit)

def show(name):
    print("Process name is:%s "% name)
    logger.debug('test debug')



def label(body):
    begintime = body.decode().split('--',1)[0]
    endtime = body.decode().split('--',1)[1]
    cmds = body.decode().split('--',1)
    print(begintime+endtime)
    return cmds

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    CMDs = label(body)
    print(CMDs)

    ch.basic_ack(delivery_tag=method.delivery_tag)

    for CMD in CMDs:
        p = Process(target=show, args=(CMD,))

        p.start()
        p.join()
        print(p.pid)






channel.basic_consume('hello',
                      callback,
                      auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()