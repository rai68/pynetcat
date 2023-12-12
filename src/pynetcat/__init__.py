import socket

class pynetcat:
    def __init__(self, options = {}):
        self.host = ''
        self.port = 0
        self.loglevel = 2
        self.ipv = socket.AF_INET
        self.buffmax = 8192
        self.encoding = options.get('encoding')  or 'utf-8'
        self.loglevel = options.get('loglevel') or 2
        self.timeout = options.get('timeout') or 20
        
        self.buffer = b''
        
        
        if options.get("ipv") == 4:
            self.ipv = socket.AF_INET
        elif options.get("ipv") == 6:
            self.ipv = socket.AF_INET6
        try:
            self.logger(f'Creating socket for netcat',1)
            self.socket = socket.socket(self.ipv, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
        except Exception as e:
            return e

    def connect(self, host,port):
        #connect to host and port + init the socket assuming mode is client
        # returns true if sucessful or error if failed
        try:
            self.logger(f"Connecting to socket at {host}:{port}",1)
            self.host = host
            self.port = port
            self.socket.connect((host,port))
            self.logger(f"Connected to socket at {host}:{port} successfully.",1)
            return True
        except Exception as e:
            self.logger(f"An error coccured while connecting to the socket: {e}",2)
            return e

    def send(self, message):
        if type(message) != bytes:
            self.logger("Passed 'message' must be a bytes object",2)
            return Exception("Passed 'message' must be a bytes object")
        #will send message to the socket server without a newline
        try:
            self.socket.sendall(message)
        except Exception as e:
            
            return e

    def sendLine(self, message = ""):
        if type(message) != bytes:
            self.logger("Passed 'message' must be a bytes object",2)
            return Exception("Passed 'message' must be a bytes object")
        #will send message to the server as a newline
        message += b'\n'  # Adding newline as a delimiter
        try:
            self.socket.sendall(message)
        except Exception as e:
            return e

    def receive(self, size = 8192):
        if size < self.buffmax:
            self.logger(f"Size is greater than max ({self.buffmax})",2)
            return Exception(f"Size is greater than max ({self.buffmax})")
        size = self.buffmax
        self.buffer = self.socket.recv(size)
        return self.buffer

    def receiveUntil(self,until,size = 8192,keep = True):
        if size < self.buffmax:
            self.logger(f"Size is greater than max ({self.buffmax})",2)
            return Exception(f"Size is greater than max ({self.buffmax})")
        if type(until) != bytes:
            self.logger("Passed 'until' must be a bytes object",2)
            return Exception("Passed 'until' must be a bytes object")
        sizeL = size or self.buffmax
        self.buffer = b''
        buff = b''
        try:
            while until not in buff or len(buff) > sizeL:
                buff = buff + self.socket.recv(1)
            if keep is False:
                buff = buff[:-len(until)]
            self.buffer = buff
            return buff
        except Exception as e:
            self.logger(f"Failed to receive until: {e}",2)

    def close(self):
        self.logger("Closing connection on socket",1)
        try:
            self.socket.close()
        except Exception as e:
            self.logger(f"Failed to close socket: {e}")

    def logger(self, log, level):
        if self.loglevel > 0 and level == 1:
            print(f"[Info]  : " + log)
        if self.loglevel > 1 and level == 2:
            print(f"[Error] : " + log)
            
            
            
            
from pynetcat import pynetcat
import sys
from threading import Thread
nc = pynetcat({'timeout':500,'loglevel':0})
print("--------------------------------------------------------------------")
print("pyNetcat CLI - a Python based netcat utility that works on windows")
print("Import pynetcat from this file for a module based utility.")
print("--------------------------------------------------------------------")

host = input("Hostname: ")
port = int(input("Port: "))

nc.connect(host,port)

def loop():
    while(1):
        line = nc.receive(8192).decode()
        if len(line) != 0:
            print(line,end="")
t1 = Thread(target=loop)
t1.daemon = True
t1.start()

while(1):
    nc.sendLine(input().encode(nc.encoding))