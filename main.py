from remoteControl import RemoteControl
from pprint import pprint
from time import sleep
from gpio import GPIOHandler
import signal
from threading import Event

def doWhenDone():
    print("do when done")

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

def main():
    rc = RemoteControl('/home/pi/mp3s',doWhenDone)
    gp = GPIOHandler(rc)
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    # Run forever!
    Event().wait()

if __name__ == "__main__":
    main()
