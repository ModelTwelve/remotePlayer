from remoteControl import RemoteControl
from pprint import pprint
from threading import Thread
from time import sleep
from buttonTestServer import ButtonTestServer
import socket
import asyncore


def startButtonServer(rc):
    buttonServer = ButtonTestServer('localhost', 8080, rc)
    asyncore.loop(timeout=1)
    print("done")

def doWhenDone():
    print("done playing")

def main():
    rc = RemoteControl('/home/kenny/Desktop/mp3',doWhenDone)
    buttonServerThread = Thread(target = startButtonServer, args=(rc,))
    buttonServerThread.start()
    # Run forever!
    buttonServerThread.join()    
    #rc.Play('/home/kenny/Desktop/mp3/1980 - Back In Black/06 - Back In Black.mp3')
    #sleep(5)
    asyncore.close_all()    
    print("thread finished...exiting")

if __name__ == "__main__":
    main()
