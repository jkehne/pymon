#!/usr/bin/env python

import pynotify
import socket
import sys
import time

while True:
    try:
        sock = socket.create_connection(("fritz.box",1012))
    except socket.error, msg:
        #print("Connect failed")
        time.sleep(60)
        continue
    break

pynotify.init("Callmonitor")

while True:
    data = sock.recv(1024)

HelloNotification = pynotify.Notification("Hello World!","This is my first notification messsage","dialog-information")
HelloNotification.show()
