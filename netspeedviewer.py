#! usr/bin/python
# -*- coding=utf-8 -*-

'''
This module is developed for a view of network speed.
'''

from tkinter import *
import psutil


class AppUI(Frame):
    def __init__(self, master, downspeed='0 KB/S', upspeed='0 KB/S'):
        Frame.__init__(self, master)
        self.downSpeed = StringVar()
        self.downSpeed.set(downspeed)
        self.upSpeed = StringVar()
        self.upSpeed.set(upspeed)
        self.pack()
        self.setRootAttrs()
        self.createWidgets()

    def setRootAttrs(self):
        self.master.overrideredirect(True)
        self.master.geometry("140x20+1226+708")
        self.master.attributes("-alpha", 0.7)
        self.master.wm_attributes('-topmost', 1)

    def createWidgets(self):
        self.downLabel = Label(self, fg='red', textvariable=self.downSpeed)
        self.downLabel.pack(side=LEFT)
        self.upLabel = Label(self, fg='green', textvariable=self.upSpeed)
        self.upLabel.pack(side=LEFT)


class Application(AppUI):
    def __init__(self, master=None):
        AppUI.__init__(self, master)
        self.downPast = psutil.net_io_counters().bytes_recv
        self.upPast = psutil.net_io_counters().bytes_sent
        self.bind('<Double-Button-1>', exitApp)
        self.after(1000, self.setSpeed)

    def setSpeed(self):
        nowdown = psutil.net_io_counters().bytes_recv
        nowup = psutil.net_io_counters().bytes_sent
        downspeed = (nowdown - self.downPast)/1000
        upspeed = (nowup - self.upPast)/1000
        self.downSpeed.set('%.1f KB/S' % downspeed)
        self.upSpeed.set('%.1f KB/S' % upspeed)
        self.downPast = nowdown
        self.upPast = nowup
        self.after(1000, self.setSpeed)


def exitApp(event):
    app.quit()
    app.master.destory()



app = Application()
app.master.bind('<Key>', exitApp)
app.mainloop()