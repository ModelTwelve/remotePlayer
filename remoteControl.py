import pexpect
import os
from threading import Thread
from threading import Lock
from time import sleep
from random import shuffle

class RemoteControl():

    Current = 0    
    ACTIVELY_PLAYING = False
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
        if self.ACTIVELY_PLAYING:            
            self.Pause()
        else:
            self.ACTIVELY_PLAYING=True
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
        self.ACTIVELY_PLAYING=False
    
    def Stop(self):
        self.RemoteControlProcess.send("S\r") 

    def Pause(self):
        self.RemoteControlProcess.send("P\r") 

    def Prev(self):
        self.Stop()
        if self.Current > 0:
            self.Current -= 1
        else:
            self.Current = len(self.Playlist)-1
        self.ACTIVELY_PLAYING=False
        self.Play()      
    
    def Next(self):
        self.Stop()
        if self.Current < len(self.Playlist)-1:
            self.Current += 1
        else:
            self.Current=0
        self.ACTIVELY_PLAYING=False
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

