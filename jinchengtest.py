import time
import logging
from multiprocessing import Process

logging.basicConfig(format='%(asctime)s - %(process)d - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)




def A(num):
    while True:
        print('正在调用函数%d'%num)
        time.sleep(1)

for i in range(10):
    p = Process(target = A, args = (i,)) #创建进程对象,并指定进程将来要执行的函数.
    p.start() #启动进程.
    logging.debug('debug 信息')
    logging.info('info 信息')
    logging.warning('warning 信息')
    logging.error('error 信息')
    logging.critical('critial 信息')
    print(p.pid)

