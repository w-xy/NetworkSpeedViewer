#! usr/bin/python
# -*- coding=utf-8 -*-

'''
This module is developed for a view of network speed.
'''

import time
import psutil


def speed_producer(looptimes):
    '''
    network speed is produced here.
    '''
    pastdown = psutil.net_io_counters().bytes_recv
    pastup = psutil.net_io_counters().bytes_sent
    while looptimes:
        nowdown = psutil.net_io_counters().bytes_recv
        nowup = psutil.net_io_counters().bytes_sent
        downspeed = (nowdown - pastdown)/1000
        upspeed = (nowup - pastup)/1000
        print('Down %.1f  Up %.1f' % (downspeed, upspeed))
        pastdown = nowdown
        pastup = nowup
        looptimes -= 1
        time.sleep(1)


if __name__ == '__main__':
    speed_producer(100)
