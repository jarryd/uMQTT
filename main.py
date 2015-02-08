#=========================================================================================

__author__ = "Jarryd Bekker"
__copyright__ = "Copyleft 2013, Bushveld Labs"

__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jarryd Bekker"
__email__ = "jarryd@bushveldlabs.com"
__status__ = "Development"

#=========================================================================================

# To do:

#=========================================================================================

# Python modules
import sys
import socket

# Third party modules
import time

# Custom modules
import uMQTT

#=========================================================================================

if __name__ == "__main__":

    MQTT_SERVER = "iot.eclipse.org"
    MQTT_PORT = 1883
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    s.connect((MQTT_SERVER, MQTT_PORT))
    

    # Create connect message
    ConnectMsg = uMQTT.Connect(clientID = "someClientID")
                            
    # Create publish message
    PublishMsg = uMQTT.Publish(topic = ('testtopic/subtopic'), payload = 'Hello World!', qos = 0)
                            
    # Create disconnect message
    DisconnectMsg = uMQTT.Disconnect()

    
    s.send(ConnectMsg.Assemble())
    data = s.recv(100)
    print(data, hex) # Should return ' \x02\x00\x00' if connection is accepted
    
    s.send(PublishMsg.Assemble())
    
    s.send(DisconnectMsg.Assemble())
    
        