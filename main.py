from remoteControl import RemoteControl
from pprint import pprint
from threading import Thread
from time import sleep
from buttonTestServer import ButtonTestServer
import socket
import asyncore

def startButtonServer():
    buttonServer = ButtonTestServer('localhost', 8080)
    asyncore.loop(timeout=1)
    print("done")

def main():
    buttonServerThread = Thread(target = startButtonServer)
    buttonServerThread.start()

    rc = RemoteControl()
    rc.Play('/home/kenny/Downloads/SampleAudio_0.7mb.mp3')
    sleep(5)
    rc.Play('/home/kenny/Downloads/SampleAudio_0.7mb.mp3')
    sleep(5)
    rc.Stop()

    asyncore.close_all()
    
    buttonServerThread.join()
    print("thread finished...exiting")

if __name__ == "__main__":
    main()