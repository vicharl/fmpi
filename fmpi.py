#!/usr/bin/env python
#coding=utf-8

import os
import time
import random
import config
import subprocess
from db import DB
from get_sogou_mp3 import getlink

class FMPI(DB):
    '''从播放队列获取歌曲并播放'''
    def play(self,name_or_url,freq=97.5,rate=44100):
        '''调用外部播放命令'''
        cmd = "mpg123 -m -C -q -s %s | sudo pifm - %s %s"%(name_or_url,freq,rate)
        p1 = subprocess.Popen(cmd,shell=True)
        p1.wait()
        print p1.pid
#        os.system(cmd)
        return 0

    def get_random_music(self):
        music_set = file("./music_name.txt").readlines()
        total = len(music_set)
        rand = random.randint(0,total-1)
        return music_set[rand][:-1]

    def fmpi(self):
        '''循环检测'''
        while True:
            query = DB.getall(self)
            try:
                one = query[0]
            except:
                one = None
            if one is not None:
                url = getlink(one[1].encode('utf-8'))
                self.play(url,config.freq,config.rate)
                DB.updateone(self,one[0])
            else:
                rand_music = self.get_random_music()
                DB.put(self,rand_music)
            time.sleep(1)#降低CPU占用率

