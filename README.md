

# Python based netcat utility

A really simple tool for CTFs, just import and run with no fuss.

## Install
`pip install --upgrade pynetcat`

## Examples
### Import as module
```
from pynetcat import pynetcat
nc = pynetcat()
host = 'example.host'
port = 9999
nc.connect(host,port)
print(nc.receive(8192).decode())
nc.sendLine(b"Message Here")
```
### Run as netcat CLI tool for windows
`python -m pynetcat`
