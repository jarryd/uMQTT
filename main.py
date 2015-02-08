#=========================================================================================

__author__ = "Jarryd Bekker"
__copyright__ = "Copyleft 2015, Bushveld Labs"

__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jarryd Bekker"
__email__ = "jarryd@bushveldlabs.com"
__status__ = "Development"

#=========================================================================================

# To do:

#=========================================================================================

# Python modules
import socket

# Third party modules

# Custom modules
import uMQTT

#=========================================================================================

if __name__ == "__main__":

    MQTT_SERVER = "iot.eclipse.org"
    MQTT_PORT = 1883
    
    # Create a socket connection to the server and connect to it
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Try connect to the socket

    s.connect((MQTT_SERVER, MQTT_PORT))

    # Send a CONNECT message
    s.send(uMQTT.CONNECT(client_id = "someClientID").assemble())
    rsps = s.recv(100)
    
    # Print the response message
    print(uMQTT.CONNACK().parse(response = rsps)[1])
        
    # Send a PUBLISH message
    s.send(uMQTT.PUBLISH(topic = 'testtopic/subtopic', payload = 'Hello World!', qos = 0).assemble())

    # Send a DISCONNECT message
    s.send(uMQTT.DISCONNECT().assemble())
