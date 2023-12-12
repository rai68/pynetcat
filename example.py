from pynetcat import pynetcat

nc = pynetcat()

host = 'example.host'
port = 9999

nc.connect(host,port)

print(nc.receive(8192).decode())

nc.sendLine(b"Message Here")
