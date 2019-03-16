import asyncore
import socket
from time import sleep

class ButtonTestHandler(asyncore.dispatcher_with_send):
    rc = None

    def handle_read(self):
        data = self.recv(8192)
        if data:
            cmd = data.decode("utf-8").upper()
            if cmd.startswith("PLAY"):
                self.rc.Play()
            elif cmd.startswith("NEXT"):
                self.rc.Next()
            elif cmd.startswith("PREV"):
                self.rc.Prev()
            elif cmd.startswith("PAUSE"):
                self.rc.Pause()
            elif cmd.startswith("UNPAUSE"):
                self.rc.Pause()
            elif cmd.startswith("STOP"):
                self.rc.Stop()
                self.rc.InitList()
            self.send(data)

class ButtonTestServer(asyncore.dispatcher):
    rc = None
    def __init__(self, host, port, rc1): 
        self.rc = rc1       
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = ButtonTestHandler(sock)
            handler.rc = self.rc

