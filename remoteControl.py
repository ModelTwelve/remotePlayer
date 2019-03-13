import pexpect

from threading import Thread
from time import sleep

class RemoteControl():

    SPAWNPROCESS = '/usr/bin/mpg123 -R'    
    QUIT = "q\r"

    def __init__(self):      
        self.RemoteControlProcess = pexpect.spawn(self.SPAWNPROCESS)  

        self.MonitorProcessThread = Thread(target=self.MonitorProcess)
        self.MonitorProcessThread.start()

    def Play(self, filename):
        cmd = "LOAD %s\r" % (filename)
        self.RemoteControlProcess.send(cmd) 

    def MonitorProcess(self):
        self.RemoteControlProcess.expect([pexpect.TIMEOUT, pexpect.EOF])           

    def Stop(self):
        self.RemoteControlProcess.send(self.QUIT)
        self.RemoteControlProcess.terminate(force=True)

    def DoThis(self, volume):
        raise NotImplementedError

