#!/usr/bin/env python

import paho.mqtt.client as mqtt
import time
import json
import subprocess
import sys 
import shlex

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print output.strip()
    rc = process.poll()
    return rc


def create_firewall(device, location):
    print("	Creating Device: device = " + device + " location = " + location)
    run_command("ls -la")


def delete_firewall(device, location):
    print("	Deleting Device: device = " + device + " location = " + location)

def block_category(category, device, location):
    print("	Blocking " + category + " on device " + device + " in location " + location)


def on_message(client, userdata, message):

    message_string = str(message.payload.decode("utf-8"))
    message_dict = json.loads(message_string)

    action = message_dict["data"][0]["action"]
    what = message_dict["data"][0]["what"]
    #where = message_dict["data"][0]["where"]

    print("--- New MQTT Message. Action = " + action + " What = " + what)

    if (action == "create-for-in"):
        if " in " not in what:
            print("   Command not in right syntax: " + what)
            return

        device = what.split(" in ")[0]
        location = what.split(" in ")[1] 
       
        #print("   Creating " + device + " in " + location)
        create_firewall(device, location)

    elif (action == "delete-for-in"):
        if " in " not in what:
            print("   Command not in right syntax: " + what)
            return
        elif " firewall in " in what:
            device = what.split(" firewall in ")[0]
            location = what.split(" firewall in ")[1]
        else:
            device = what.split(" in ")[0]
            location = what.split(" in ")[1]

        #print(" Deleting device " + device + " in " + location)
        delete_firewall(device, location)
  
    elif (action == "block"):
        # Format of message coming in is "CATEGORY on DEVICE in LOCATION", so split it that way
        tmp = what.split(" on ")
        category = tmp[0]
        device = tmp[1].split(" in ")[0]
        location = tmp[1].split(" in ")[1]

        block_category(category, device, location)

    elif (action == "RADIUS-START"):
        # radius-msg is a dictionary, i.e. radius["NAS-Identifer"] == 'iPhone8'.
        radius = dict(item.split("=") for item in what.split(";"))
        # strip the single quotes out of the message
        for key in radius:
	     radius[key] = radius[key].replace("'", "")

	# These are the fields:
        #print(radius["User-Name"])
        #print(radius["NAS-IP-Address"])
        #print(radius["Framed-IP-Address"])
        #print(radius["NAS-Identifier"])

        if (radius["NAS-IP-Address"] == "1.1.1.1"):
	    location = "Melbourne"
        elif (radius["NAS-IP-Address"] == "2.2.2.2"):
	    location = "Sydney"
        else:
	    location = "Perth"

	create_firewall(radius["User-Name"], location) 


    elif (action == "RADIUS-STOP"):
        # radius-msg is a dictionary, i.e. radius["NAS-Identifer"] == 'iPhone8'.
        radius = dict(item.split("=") for item in what.split(";"))
        # strip the single quotes out of the message
        for key in radius:
             radius[key] = radius[key].replace("'", "") 

	# These are the fields:
        #print(radius["User-Name"])
        #print(radius["NAS-IP-Address"])
        #print(radius["Framed-IP-Address"])
        #print(radius["NAS-Identifier"])

        if (radius["NAS-IP-Address"] == "1.1.1.1"):
            location = "Melbourne"
        elif (radius["NAS-IP-Address"] == "2.2.2.2"):
            location = "Sydney"
        else:
            location = "Perth"

        delete_firewall(radius["User-Name"], location) 


    # print("--- New MQTT Message. Action = " + action + " What = " + what + " Where = " + where)

    # DEBUGGING Messages, use if needed.
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successful connection to MQTT broker. Waiting for messages...")
    else:
        print("Connection failed")
        exit

#def on_log(client, userdata, level, buf):
#  print("log: ",buf)

# BeeBotte credentials & channel details
broker_address="mqtt.beebotte.com"
port="1883"
user="token:token_XXXX"
password=""
channel="junipersdn/bucket"

# Create new mqtt instance
client = mqtt.Client("P1")
client.username_pw_set(user, password=password)

# Attach functions for callbacks during interrupts:
client.on_connect = on_connect # This is used during connections only
client.on_message=on_message # This is used for receiving all messages
#client.on_log=on_log # Used for some logging / debugging purposes

# Connect to the broker
print("Trying to connect to broker")
client.connect(broker_address, port=port)
client.loop_start()

# Subscribe to the MQTT channel
print("Subscribing to channel " + channel)
client.subscribe(channel)


# Loop while waiting for messages to interrupt with the MQTT.loop_start && the on_message function
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()


# Sending a message to the MQTT channel
#print("Publishing message to topic", channel)
#client.publish(channel,"OFF")
