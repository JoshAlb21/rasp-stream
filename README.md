Project from 2020

## General:

client: eg. RaspberryPi
server: eg. Laptop

requirements:
* -Client and server must be connectable via a TCP socket
* -check connection with server_test.py and client_test.py by hand

Disclaimer!:
* -Designations "client" and "server" are reversed in relation to the "socket" module (i.e. RaspberryPi waits for the laptop to connect to it)

Instructions
1. choose settings in server/server_settings.py
2. starte client/send_data.py
3. starte server/video_receiver.py

## Bugs (to be fixed):

1. data might received faster than server is able to process
