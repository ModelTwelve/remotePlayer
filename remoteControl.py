import pexpect
import os
from threading import Thread
from time import sleep
from random import shuffle

class RemoteControl():

    SPAWNPROCESS = '/usr/bin/mpg123 -R'    
    QUIT = "q\r"

    def __init__(self, MP3Dir, callback):        
        self.Current=0
        self.MP3Dir = MP3Dir
        self.InitList()
        self.callback = callback
        self.RemoteControlProcess = pexpect.spawn(self.SPAWNPROCESS, timeout=None)  

        self.MonitorProcessThread = Thread(target=self.MonitorProcess)
        self.MonitorProcessThread.start()

    def Play(self):
        cmd = "LOAD %s\r" % (self.Playlist[self.Current])
        self.RemoteControlProcess.send(cmd) 
    
    def InitList(self): 
        self.Playlist = []
        for dirname, dirnames, filenames in os.walk(self.MP3Dir):        
            for filename in filenames:
                if filename.lower().endswith(".mp3"):
                    self.Playlist.append(os.path.join(dirname, filename))
        shuffle(self.Playlist)
        self.Current=0    
    
    def Stop(self):
        self.RemoteControlProcess.send("S\r") 

    def Pause(self):
        self.RemoteControlProcess.send("P\r") 

    def Prev(self):
        self.Stop()
        self.Current -= 1
        self.Play()      
    
    def Next(self):
        self.Stop()
        self.Current += 1
        self.Play()        

    def MonitorProcess(self):
        ev=999
        while ev > 1:
            ev = self.RemoteControlProcess.expect(
                [        
                    pexpect.TIMEOUT, 
                    pexpect.EOF,
                    "@P 0",
                ])
            if ev == 2:
                self.callback()


    def Quit(self):
        self.RemoteControlProcess.send(self.QUIT)
        self.RemoteControlProcess.terminate(force=True)

    def DoThis(self, volume):
        raise NotImplementedError

