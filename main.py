from remoteControl import RemoteControl
from pprint import pprint
from threading import Thread
from time import sleep
from buttonTestServer import ButtonTestServer
import socket
import asyncore
from gpio import GPIOHandler

def startButtonServer(rc):
    buttonServer = ButtonTestServer('localhost', 8080, rc)
    asyncore.loop(timeout=1)
    print("done")

def doWhenDone():
    print("done playing")

def main():
    rc = RemoteControl('/home/pi/mp3s',doWhenDone)
    gp = GPIOHandler(rc)
    buttonServerThread = Thread(target = startButtonServer, args=(rc,))
    buttonServerThread.start()
    # Run forever!
    buttonServerThread.join()    
    asyncore.close_all()    
    print("thread finished...exiting")

if __name__ == "__main__":
    main()
