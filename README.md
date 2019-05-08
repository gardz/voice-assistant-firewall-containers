# Google Assistant / Google Home paired with Container Firewalls

This was designed to link a voice assistant such as Google Assistant to

# Architecture 

This uses If This Then That (IFTTT) to hook voice commands from Google Assistant, and translate values from the spoken verbal command into a JSON payload that is pushed onto an MQTT message bus. A micro-service is listening to the message bus to pick up the resulting commands to then carry out the relevant actions. 

This decouples the solution into a couple of independent micro-services to simplify & speed up development:
- ifttt: the "cloud glue" that links Google Home to the MQTT Message Bus.
- mqtt-subscriber.py: listen to the MQTT message bus to pull off specific commands that were pushed on via Google Home.
- actions.py: take input values and actions from the messages on the bus and carry out resulting actions (i.e. create containerised firewall, push new security policy to a specific firewall, etc). 


# Extra Notes

Sign up to:
  IFTTT.com: to simplify linking Google Home into the Message Bus
  BeeBotte.com: the MQTT as a Service. And it's super generous with the number of messages allowed on the free plan. 
  
Add the various tokens and channels for BeeBottee in mqtt-subscriber.py. 
