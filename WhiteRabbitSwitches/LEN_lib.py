# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 09:06:47 2022

@author: qlab
"""

import time
import numpy as np
import serial
from datetime import datetime, timezone


class dev:
    def __init__(self, serialport=''):
        self.wrs = serial.Serial(serialport, 115200, timeout=0.25, bytesize=8, stopbits=1)
        print('Connecting to WRS')

    def write(self, msg):
        self.wrs.write(msg.encode())

    def read(self):
        msg = self.wrs.read(20000)
        try:
            ret = msg.decode()
        except UnicodeDecodeError:
            ret = '-1'
        return ret

    def getStat(self):
        self.write('stat\r')
        time.sleep(1)
        ret = self.read()
        return ret

    def getDate(self):
        self.write('time\r')
        ret = self.read()

        tai = ret.split('\n')[1].split('+')[0][:-1]

        tai_timestamp = datetime.timestamp(datetime.strptime(tai, "%a, %b %d, %Y, %H:%M:%S").replace(tzinfo=timezone.utc))
        temp = datetime.fromtimestamp(tai_timestamp)
        tai_date = temp.strftime("%Y-%m-%d %H:%M:%S")
        temp = datetime.fromtimestamp(tai_timestamp - 37)
        utc_date = temp.strftime("%Y-%m-%d %H:%M:%S")
        return [tai_timestamp, tai_date, utc_date]

    def close(self):
        self.wrs.close()


if __name__ == '__main__':
    WRS = dev('COM4')
    ret = WRS.get_date()
    print(ret[0])
    WRS.close()


