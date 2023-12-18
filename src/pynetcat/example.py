from pynetcat import pynetcat

nc = pynetcat()

host = 'example.host'
port = 9999

nc.connect(host,port)

print(nc.receive(8192).decode())

nc.send(b"Message no newline")

nc.sendLine(b"Message Here")

Size = 1024
print(nc.receive(Size))
print(nc.receiveUntil(b"ABCD", Size))

