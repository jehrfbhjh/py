#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                       exchange_type='topic')

routing_key = ['#', "kern.critical", "A critical kernel error"]
for i in range(10):
     message = '{} msg at : routing key {}'.format(i, routing_key[i % 3])
     channel.basic_publish(exchange='topic_logs',
                           routing_key=routing_key[i % 3],
                           body=message)
     print(" [x] Sent :%r" % (message))
connection.close()
