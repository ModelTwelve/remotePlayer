import pexpect
import os
from threading import Thread
from threading import Lock
from time import sleep
from random import shuffle

class RemoteControl():

    Genre = 1
    Current = [ 0,0,0 ]    
    ACTIVELY_PLAYING = False
    PAUSED = False
    SPAWNPROCESS = '/usr/bin/mpg123 -R'    
    QUIT = "q\r"

    def __init__(self, MP3Dir, callback):   
        self.MP3Dir = MP3Dir
        self.InitList()
        self.callback = callback
        self.RemoteControlProcess = pexpect.spawn(self.SPAWNPROCESS, timeout=None)  

        self.MonitorProcessThread = Thread(target=self.MonitorProcess)
        self.MonitorProcessThread.start()

    def Play(self):        
        if self.ACTIVELY_PLAYING:            
            if self.PAUSED:
                self.UnPause()
            else:
                self.Pause()
        else:
            self.ACTIVELY_PLAYING=True
            self.PAUSED=False;
            print("Play {},{}".format(self.Genre,self.Current[self.Genre]))
            cmd = "LOAD %s\r" % (self.Playlist[self.Genre][self.Current[self.Genre]])            
            self.RemoteControlProcess.send(cmd) 

    def InitInnerList(self, rockgenre, listnumber):
        for dirname, dirnames, filenames in os.walk(os.path.join(self.MP3Dir,rockgenre)):                    
            for filename in filenames:
                if filename.lower().endswith(".mp3"):
                    print("Adding {}".format(filename))
                    self.Playlist[listnumber].append(os.path.join(dirname, filename))        
        shuffle(self.Playlist[listnumber])

    def PlayGenre(self):        
        if self.Genre == 0:
            os.system("omxplayer --vol -1204 /home/pi/sounds/Soft.m4a")
        elif self.Genre == 1:
            os.system("omxplayer --vol -1204  /home/pi/sounds/Classic.m4a")
        elif self.Genre == 2:
            os.system("omxplayer --vol -1204  /home/pi/sounds/Heavy.m4a")

    def InitList(self): 
        self.Playlist = [ [], [], [] ]

        self.InitInnerList("soft", 0) 
        self.InitInnerList("classic", 1) 
        self.InitInnerList("heavy", 2)        
        
        self.Current = [0,0,0]
        self.ACTIVELY_PLAYING=False
        self.PAUSED=False
    
    def Stop(self):
        self.ACTIVELY_PLAYING=False
        self.PAUSED=False
        self.RemoteControlProcess.send("S\r") 

    def Pause(self):
        if self.ACTIVELY_PLAYING and not self.PAUSED:   
            self.PAUSED = True
            self.RemoteControlProcess.send("P\r") 
    
    def UnPause(self):
        if self.ACTIVELY_PLAYING and self.PAUSED:   
            self.PAUSED = False
            self.RemoteControlProcess.send("P\r") 

    def Prev(self):
        if self.Current[self.Genre] > 0:
            self.Current[self.Genre] -= 1
        else:
            self.Current[self.Genre] = len(self.Playlist[self.Genre])-1
        self.ACTIVELY_PLAYING=False
        self.PAUSED=False
        self.Play()      
    
    def Next(self):
        if self.Current[self.Genre] < len(self.Playlist[self.Genre])-1:
            self.Current[self.Genre] += 1
        else:
            self.Current[self.Genre]=0
        self.ACTIVELY_PLAYING=False
        self.PAUSED=False
        self.Play()        
    
    def PrevGenre(self):        
        self.Stop()
        if self.Genre > 0:
            self.Genre -= 1
        else:
            self.Genre = len(self.Playlist)-1        
        self.PlayGenre()        

    def NextGenre(self):        
        self.Stop()
        if self.Genre < len(self.Playlist)-1:
            self.Genre += 1
        else:
            self.Genre = 0        
        self.PlayGenre()

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
                if self.ACTIVELY_PLAYING:   
                    self.callback()
                    self.Next()
            print("MonitorProcess {}".format(ev))

    def Quit(self):
        self.RemoteControlProcess.send(self.QUIT)
        self.RemoteControlProcess.terminate(force=True)

    def DoThis(self, volume):
        raise NotImplementedError

