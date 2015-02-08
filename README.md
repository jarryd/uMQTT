# uMQTT

uMQTT is a lightweight MQTT library for Python. It was intended for lightweight embedded systems running older versions of Python (V2.4+).

This implementation is based on the [MQTT V3.1 Protocol Specification.](http://public.dhe.ibm.com/software/dw/webservices/ws-mqtt/mqtt-v3r1.html)

The current implementation supports the following command messages:

* CONNECT
* PUBLISH
* DISCONNECT

The following command messages will be added in future revisions:

* CONNACK
* PUBACK
* PUBREC
* PUBREL
* PUBCOMP
* SUBSCRIBE
* SUBACK
* UNSUBSCRIBE
* UNSUBACK
* PINGREQ
* PINGRESP

# Getting Started (Mac)

First, you're going to need Python 2.4. This can be downloaded [here](https://www.python.org/ftp/python/2.4.3/Universal-MacPython-2.4.3-2006-04-07.dmg).

I'm using multiple versions of Python on my Mac, so I had to create an alias to python 2.4 before I could run the main.py example code. This can be done as follows:

> alias python24='/Library/Frameworks/Python.framework/Versions/2.4/bin/python'

Next, run main.py in python 2.4:

> python24 main.py
