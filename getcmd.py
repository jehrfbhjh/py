# -*- coding: utf-8 -*-
import os
import sys
# 更改当前路径
# os.chdir('/home/hust/PycharmProjects/HuashuGit/src')
#os.chdir('C:\\Users\\KeLe\\PycharmProjects\\huashu_label\\src')
#sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import pika
import logging.config
# from multiprocessing import Process
import threading
from python_logging_rabbitmq import RabbitMQHandler
#from cmptTFIDFAdv import callByRabbit
thread_no=1
# log初始化
# 读取日志配置文件内容
logging.config.fileConfig('/Users/wangshuaishuai/PycharmProjects/py/logging.conf')
# 创建一个日志器logger
logger = logging.getLogger('simpleExample')

# 将消息队列的句柄加入日志系统
#rabbit = RabbitMQHandler(host='localhost', port=5672)
#rabbit = RabbitMQHandler(queue="hello10",host='localhost', port=5672, username="guest", password="guest", exchange='',
#                        formatter=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
#logger.addHandler(rabbit)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 连接消息队列服务器
#credentials = pika.PlainCredentials("hust", "hust")
#connection = pika.BlockingConnection(pika.ConnectionParameters(
#    host='222.20.79.153', port=5679, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, beginTime, endTime):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.beginTime = beginTime
        self.endTime = endTime

    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # pid = os.getpid()
        # logTest = "My Process ID is: %s" % pid
        while True:
            # logger.addHandler(rabbit)
            logTest = "My Process ID is: %s --------" % self.threadID
            logTest = logTest + "My Thread name is : %s" % self.name

            logger.info(logTest)
            logger.info(" Execute python file now")
            #logger.addHandler(rabbit)

        #callByRabbit(self.beginTime, self.endTime)



def callback(ch, method, properties, body):

    # print("%r:%r"%(method.routing_key, body))
    # CMD = label(body)
    # callByRabbit()
    # 从数据流转为字符串
    body = body.decode().split('--',2)
    beginTime = body[0]
    endTime = body[1]
    thread_no = body[2]


    #接收线程ID并创建相应队列
    ch.basic_ack(delivery_tag=method.delivery_tag)
    rabbit = RabbitMQHandler(queue="Thread-%s" % thread_no, host='localhost', port=5672, username="guest",
                             password="guest",
                             exchange='',
                             formatter=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",
                                                         "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(rabbit)
    # 创建新线程
    thread = myThread(thread_no, "Thread-%s" % thread_no, beginTime, endTime)
    thread.start()



    # 开启线程




channel.basic_consume('hello', callback, auto_ack=False)
#logger.info('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
