#!/usr/bin/python -u

# Copyright 2012 Jens Kehne
#
# PyMon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# PyMon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyMon.  If not, see <http://www.gnu.org/licenses/>.

import pynotify
import socket
import sys
import time
import httplib
import json

API_KEY = "b1039fe5c0abbe48596785a8ea25e9d5"
FRITZBOX_ADDRESS = "192.168.178.1"

pynotify.init("PyMon")

while True:
    while True:
        print("Connecting\n")
        try:
            sock = socket.create_connection((FRITZBOX_ADDRESS,1012))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 60)
            sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 60)
            sock.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 2)
        except:
            print("Connect failed\n")
            time.sleep(60)
            continue
        break
    
    print("Connected\n")

    while True:
        try:
            data = sock.recv(1024)
        except:
            break
        print(data)
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
            try:
                httpConn = httplib.HTTPConnection("openapi.klicktel.de")
                httpConn.request("GET","searchapi/invers?key={}&number={}".format(API_KEY, number))
                resp = httpConn.getresponse()
                if (resp.status == 200):
                    respData = resp.read()
                    print(respData)
                    dataArray = json.loads(respData)
                    results = dataArray["response"]["results"]
                    print(results)
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
            except:
                name = number
        
        HelloNotification = pynotify.Notification(title,
                                                  name,
                                                  "dialog-information")
        HelloNotification.show()
