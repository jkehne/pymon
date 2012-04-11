#!/usr/bin/env python

import pynotify
import socket
import sys
import time

pynotify.init("Callmonitor")

while True:
    while True:
        try:
            sock = socket.create_connection(("192.168.178.1",1012))
        except socket.error, msg:
            #print("Connect failed")
            time.sleep(60)
            continue
        break
    
    #print("Connected")

    while True:
        try:
            data = sock.recv(1024)
        except socket.error, msg:
            break
        #print(data)
        ret = data.split(";")
        if (ret[1] == "RING"):
            HelloNotification = pynotify.Notification("Ankommender Anruf",
                                                      "{}".format(ret[3]),
                                                      "dialog-information")
            HelloNotification.show()
        if (ret[1] == "CALL"):
            HelloNotification = pynotify.Notification("Abgehender Anruf",
                                                      "{}".format(ret[5].replace("#","")),
                                                      "dialog-information")
            HelloNotification.show()
