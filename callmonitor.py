#!/usr/bin/env python

import pynotify
import socket
import sys
import time
import httplib
import json

pynotify.init("Callmonitor")
#log = open("callmonitor.log","w")

while True:
    while True:
        #log.write("Connecting\n")
        try:
            sock = socket.create_connection(("192.168.178.1",1012))
        except socket.error, msg:
            #log.write("Connect failed\n")
            time.sleep(60)
            continue
        break
    
    #log.write("Connected\n")

    while True:
        try:
            data = sock.recv(1024)
        except socket.error, msg:
            break
        #log.write(data)
        ret = data.split(";")
        if (ret[1] == "RING"):
            title = "Ankommender Anruf"
            number = ret[3]
        elif (ret[1] == "CALL"):
            title = "Abgehender Anruf"
            number = ret[5].replace("#","")
        else:
            continue

        if (number == ""):
            name = "Unbekannter Anrufer"
        else:
            httpConn = httplib.HTTPConnection("openapi.klicktel.de")
            httpConn.request("GET","searchapi/invers?key=b1039fe5c0abbe48596785a8ea25e9d5&number={}".format(number))
            resp = httpConn.getresponse()
            if (resp.status == 200):
                respData = resp.read()
                #log.write(respData)
                dataArray = json.loads(respData)
                results = dataArray["response"]["results"]
                #log.write(results)
                if (results):
                    location = results[0]["entries"][0]["location"]
                    name = "{}, {}".format(
                        results[0]["entries"][0]["lastname"],
                        results[0]["entries"][0]["firstname"])

                    if location["street"]:
                        name = "{}\n{} {}".format(
                            name,
                            location["street"],
                            location["streetnumber"])

                    if location["zipcode"]:
                        name = "{}\n{} {}".format(
                            name,
                            location["zipcode"],
                            location["city"])
                else:
                    name = number
        
        HelloNotification = pynotify.Notification(title,
                                                  name,
                                                  "dialog-information")
        HelloNotification.show()
#http://openapi.klicktel.de/searchapi/invers?key=b1039fe5c0abbe48596785a8ea25e9d5&number=041 
