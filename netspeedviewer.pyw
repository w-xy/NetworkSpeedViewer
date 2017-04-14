#! python
# -*- coding=utf-8 -*-

'''
This module is developed for a view of network speed.
'''

from tkinter import *
import psutil


class AppUI(Frame):
    '''
    View-Layer: create the widgets and set the graphic attributes
    '''
    def __init__(self, master, downspeed='0 KB/S', upspeed='0 KB/S', 
                 winwidth=140, winhigh=20, winx=1226, winy=708):
        Frame.__init__(self, master)
        self.downString = StringVar(value=downspeed)
        self.upString = StringVar(value=upspeed)
        self.winX, self.winY = winx, winy
        self.winWidth, self.winHigh = winwidth, winhigh
        self.pack()
        self.setRootAttrs()
        self.createWidgets()

    def setRootAttrs(self):
        self.master.overrideredirect(True)
        sz = "%sx%s+%s+%s" % (self.winWidth, self.winHigh, self.winX, self.winY)
        self.master.geometry(sz)
        self.master.attributes("-alpha", 0.7)
        self.master.wm_attributes('-topmost', 1)

    def createWidgets(self):
        self.downLabel = Label(self, fg='red', textvariable=self.downString)
        self.downLabel.pack(side=LEFT)
        self.upLabel = Label(self, fg='green', textvariable=self.upString)
        self.upLabel.pack(side=LEFT)


class Application(AppUI):
    '''
    Logic-Layer: the algorithm and the callbacks
    '''

    def __init__(self, master=None):
        AppUI.__init__(self, master)
        self.showSpeed = True
        self.recvBytes = psutil.net_io_counters().bytes_recv
        self.sentBytes = psutil.net_io_counters().bytes_sent
        self.mouseX, self.mouseY = 0, 0
        self.bindCallbacks()

    def bindCallbacks(self):
        self.master.bind('<Double-Button-1>', quit)
        self.master.bind('<Button-1>', self.onGrabMouse)
        self.master.bind('<B1-Motion>', self.onMoveMouse)
        self.master.bind('<Button-3>', self.onClickRightMouse)
        self.master.bind('<ButtonRelease-3>', self.onReleaseRightMouse)
        self.after(1000, self.setSpeed)

    def setSpeed(self):
        counter = psutil.net_io_counters()
        if self.showSpeed:
            self.downString.set(self.getSpeed(counter.bytes_recv - self.recvBytes))
            self.upString.set(self.getSpeed(counter.bytes_sent - self.sentBytes))
        self.recvBytes, self.sentBytes = counter.bytes_recv, counter.bytes_sent
        self.after(1000, self.setSpeed)

    def getSpeed(self, delta):
        if delta < 200:
            return '%d B/S' % delta
        if delta < 800000:
            return '%.1f KB/S' % (delta/1000)
        if delta < 1000000000:
            return '%.1f MB/S' % (delta/1000000)
        return '%.1f GB/S' % (delta/1000000000)

    def onGrabMouse(self, event):
        self.mouseX, self.mouseY = event.x, event.y

    def onMoveMouse(self, event):
        self.winX += event.x - self.mouseX
        self.winY += event.y - self.mouseY
        sz = "%sx%s+%s+%s" % (self.winWidth, self.winHigh, self.winX, self.winY)
        self.master.geometry(sz)

    def onClickRightMouse(self, event):
        self.showSpeed = False
        self.downString.set('Memory')
        self.upString.set('%d %%' % psutil.virtual_memory().percent)

    def onReleaseRightMouse(self, event):
        self.showSpeed = True


def app_run():
    '''Run the Application'''
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    app_run()
