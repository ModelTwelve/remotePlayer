import pexpect
import os
from threading import Thread
from threading import Lock
from time import sleep
from random import shuffle

class RemoteControl():

    Genre = 1
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
            print("Play {},{}".format(self.Genre,self.Current))
            cmd = "LOAD %s\r" % (self.Playlist[self.Genre][self.Current])            
            self.RemoteControlProcess.send(cmd) 

    def InitInnerList(self, rockgenre, listnumber):
        for dirname, dirnames, filenames in os.walk(os.path.join(self.MP3Dir,rockgenre)):                    
            for filename in filenames:
                if filename.lower().endswith(".mp3"):
                    print("Adding {}".format(filename))
                    self.Playlist[listnumber].append(os.path.join(dirname, filename))        
        shuffle(self.Playlist[listnumber])

    def InitList(self): 
        self.Playlist = [ [], [], [] ]

        self.InitInnerList("soft", 0) 
        self.InitInnerList("classic", 1) 
        self.InitInnerList("heavy", 2)        
        
        self.Current=0
        self.ACTIVELY_PLAYING=False
    
    def Stop(self):
        self.RemoteControlProcess.send("S\r") 

    def Pause(self):
        self.RemoteControlProcess.send("P\r") 

    def Prev(self):
        if self.Current > 0:
            self.Current -= 1
        else:
            self.Current = len(self.Playlist[self.Genre])-1
        self.ACTIVELY_PLAYING=False
        self.Play()      
    
    def Next(self):
        if self.Current < len(self.Playlist[self.Genre])-1:
            self.Current += 1
        else:
            self.Current=0
        self.ACTIVELY_PLAYING=False
        self.Play()        
    
    def PrevGenre(self):
        self.Current = 0
        if self.Genre > 0:
            self.Genre -= 1
        else:
            self.Genre = len(self.Playlist)-1
        self.ACTIVELY_PLAYING=False
        self.Play()      

    def NextGenre(self):
        self.Current = 0
        if self.Genre < len(self.Playlist)-1:
            self.Genre += 1
        else:
            self.Genre = 0
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
                self.Next()
            print("MonitorProcess {}".format(ev))

    def Quit(self):
        self.RemoteControlProcess.send(self.QUIT)
        self.RemoteControlProcess.terminate(force=True)

    def DoThis(self, volume):
        raise NotImplementedError

