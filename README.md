# Google Assistant (Google Home) paired with Containerized Firewalls

This was designed to link a voice assistant such as Google Assistant / Google Home / Apple Siri / Amazon Alexa into SDN and networking use cases. This enables a more fluent interaction between technologies that have typically been under the control of only IT professionals  with high levels of training, where now any person can use every day language to enact changes.

The two use cases demonstrated here are:
- Create X number of docker container firewalls (Juniper cSRX) in specific region(s) Y, which boot up in under 2 seconds.
- Push security policies based on voice commands, for example a teacher in a classroom can request "Ok Google, stop social media for 1 hour in the classroom" which pushes the resulting Layer 7 application firewall policy in block Social Media in the Classroom in order to focus the attention of students for the 1 hour duration of that class. 

The use cases are limitless. 

# Architecture 

This uses If This Then That (IFTTT) to hook voice commands from Google Assistant, and translate values from the spoken verbal command into a JSON payload that is pushed onto an MQTT message bus. A micro-service is listening to the message bus to pick up the resulting commands to then carry out the relevant actions. 

This decouples the solution into a couple of independent micro-services to simplify & speed up development:
- ifttt: the "cloud glue" that links Google Home to the MQTT Message Bus. Why IFTTT? It made the development super fast and easy without having the need to develop a full "Actions on Google" package. 
- mqtt-subscribe.py: listen to the MQTT message bus to pull off specific commands that were pushed on via Google Home.
- actions.py: take input values and actions from the messages on the bus and carry out resulting actions (i.e. create containerised firewall, push new security policy to a specific firewall, etc). 

# Command Syntax

	Voice Command: create firewall for DEVICENAME in LOCATION
	Payload: {"data":[{"action":"create-for-in","what":"Leigh in Melbourne"}]}

	Voice Command: delete DEVICENAME in LOCATION
	Payload: {"data":[{"action":"delete-for-in","what":"Leigh in Melbourne"}]}

	Voice Command: create X new firewalls in LOCATION
	Payload: {"data":[{"action":"create","what":"X","where":"LOCATION"}]}

	Voice Command: delete X firewalls in LOCATION
	Payload: {"data":[{"action":"delete","what":"X","where":"LOCATION"}]} 

	Voice Command: delete DEVICE in LOCATION
	Payload: {"data":[{"action":"delete-for-in","what":"DEVICE in LOCATION"}]}

	Voice Command: block CATEGORY on DEVICE in LOCATION
	Payload: {"data":[{"action":"block","what":"CATEGORY on DEVICE in LOCATION}]}


# Extra Notes

Sign up to:
  IFTTT.com: to simplify linking Google Home into the Message Bus
  BeeBotte.com: the MQTT as a Service. And it's super generous with the number of messages allowed on the free plan. 
  
Add the various tokens and channels for BeeBottee in mqtt-subscriber.py. 

To retrieve values back from "the network" so the voice assistant can verbally play them back, a full "Actions on Google" (or equivalent for other services like Siri/Alexa) would need to be developed instead of using IFTTT. 

# RADIUS Payload Example (instead of Voice commands)

	RADIUS Start: {"data":[{"action":"RADIUS-START","what":"User-Name='leigh';NAS-IP-Address='1.1.1.1';Framed-IP-Address='210.10.10.10';NAS-Identifier='Google Pixel'"}]} 
	RADIUS Stop: {"data":[{"action":"RADIUS-STOP","what":"User-Name='leigh';NAS-IP-Address='1.1.1.1';Framed-IP-Address='210.10.10.10';NAS-Identifier='Google Pixel'"}]}
