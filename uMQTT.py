#=========================================================================================

__author__ = "Jarryd Bekker"
__copyright__ = "Copyleft 2015, Bushveld Labs"

__license__ = "GPL"
__version__ = ""
__maintainer__ = "Jarryd Bekker"
__email__ = "jarryd@bushveldlabs.com"
__status__ = "Development"

#=========================================================================================

# To do:

#   TODO
#=========================================================================================


# Python modules
import socket

# Third party modules

# Custom modules

#=========================================================================================

# Message types (subset of MQTT 3.1)
MSG_CONNECT = 0x10
MSG_CONNACK = 0x20
MSG_PUBLISH = 0x30
MSG_PUBACK = 0x40       # TODO
MSG_PUBREC = 0x50       # TODO
MSG_PUBREL = 0x60       # TODO
MSG_PUBCOMP = 0x70      # TODO
MSG_SUBSCRIBE = 0x80    # TODO
MSG_SUBACK = 0x90       # TODO
MSG_UNSUBSCRIBE = 0xA0  # TODO
MSG_UNSUBACK = 0xB0     # TODO
MSG_PINGREQ = 0xC0      # TODO
MSG_PINGRESP = 0xD0     # TODO
MSG_DISCONNECT = 0xE0

#=========================================================================================

class CONNECT(object):

    def __init__(self, client_id, keep_alive=60):
        self.clientID = client_id
        
        self.message_type = MSG_CONNECT
        
        self.DUP = False
        self.QoS = False
        self.retain = False
        
        self.User_name_flag = False
        self.Password_flag = False
        self.Will_RETAIN = False
        self.Will_QoS_MSB = False
        self.Will_QoS_LSB = False
        self.Will_flag = False
        self.Clean_Session = True
        
        self.protocol_name = "MQIsdp"
        self.protocol_version = chr(3)
        self.keep_alive = keep_alive
        
        # Client ID length
        self.client_id_length_MSB = chr((len(self.clientID) & 0xFF00) >> 8)
        self.client_id_length_LSB = chr((len(self.clientID) & 0x00FF))
        
        # Protocol name length
        self.protocol_name_length_MSB = chr((len(self.protocol_name) & 0xFF00) >> 8)
        self.protocol_name_length_LSB = chr(len(self.protocol_name) & 0x00FF)
        
        # Keep alive
        self.keep_alive_MSB = chr((self.keep_alive & 0xFF00) >> 8)
        self.keep_alive_LSB = chr(self.keep_alive & 0x00FF)
        

    def connect_flags(self):
    
        connect_flags = 0x00
        
        if self.User_name_flag: connect_flags = connect_flags or 0x80
        if self.Password_flag: connect_flags = connect_flags or 0x40
        if self.Will_RETAIN: connect_flags = connect_flags or 0x20
        if self.Will_QoS_MSB: connect_flags = connect_flags or 0x10
        if self.Will_QoS_LSB: connect_flags = connect_flags or 0x08
        if self.Will_flag: connect_flags = connect_flags or 0x04
        if self.Clean_Session: connect_flags = connect_flags or 0x02
        
        return chr(connect_flags)

    def fixed_header(self):
    
        header = self.message_type
        
        if self.DUP == 1: header = header or 0x08
        
        if self.QoS == 1: header = header or 0x02
        elif self.QoS == 2: header = header or 0x04
        elif self.QoS == 3: header = header or 0x06

        if self.retain == 1: header = chr(header) or 0x01

        return chr(header)

    def fixed_header_remaining_length(self):
        remaining_length = format_length(len(
            self.protocol_name_length_MSB +
            self.protocol_name_length_LSB +
            self.protocol_name +
            self.protocol_version +
            self.connect_flags() +
            self.keep_alive_MSB +
            self.keep_alive_LSB +
            self.client_id_length_MSB +
            self.client_id_length_LSB +
            self.clientID))
            
        return remaining_length
            
    def assemble(self):

        message = (self.fixed_header() +
                    self.fixed_header_remaining_length() +
                    self.protocol_name_length_MSB +
                    self.protocol_name_length_LSB +
                    self.protocol_name +
                    self.protocol_version +
                    self.connect_flags() +
                    self.keep_alive_MSB +
                    self.keep_alive_LSB +
                    self.client_id_length_MSB +
                    self.client_id_length_LSB +
                    self.clientID)      
                
        return message

#-----------------------------------------------------------------------------------------

class CONNACK(object):

    def __init__(self):
        self.message_type = MSG_CONNACK
        self.remaining_length = 0
        
        self.return_codes = {0: 'Connection Accepted',
                             1: 'Connection Refused: unacceptable protocol version',
                             2: 'Connection Refused: identifier rejected',
                             3: 'Connection Refused: server unavailable',
                             4: 'Connection Refused: bad user name or password',
                             5: 'Connection Refused: not authorized'}

    def parse(self, response):
        """ Parse CONNACK message"""
        
        if len(response) == 4:
            """ Check that the response is the expected size (should be 2 fixed header bytes
            and 2 variable header bytes)"""
        
            # Convert the hex length byte to an integer
            self.remaining_length = ord(response[1])
            
            code = ord(response[3])
            
            message = self.return_codes[ord(response[3])]
            
        else:
            # Something is wrong...
            code = ''
            message = ''
            print("ERROR: Something is wrong in the CONNACK parser. Didn't receive the correct response size")

        return code, message

#-----------------------------------------------------------------------------------------

class DISCONNECT(object):

    def __init__(self):
    
        self.message_type = MSG_DISCONNECT
        
        self.DUP = 0
        self.QoS = 0
        self.retain = 0

    def fixed_header(self):
    
        header = self.message_type
        
        if self.DUP == 1: header = header or 0x08
        
        if self.QoS == 1: header = header or 0x02
        elif self.QoS == 2: header = header or 0x04
        elif self.QoS == 3: header = header or 0x06

        if self.retain == 1: header = header or 0x01

        return chr(header)

    def assemble(self):

        message = (self.fixed_header() + "\x00")
                
        return message

#-----------------------------------------------------------------------------------------

class PUBLISH(object):

    def __init__(self, topic, payload, qos):
        self.Topic = topic
        self.Payload = payload
        self.QoS = qos
        
        self.message_type = MSG_PUBLISH
        
        self.DUP = 0
        self.QoS = 0
        self.retain = 0         

        self.TopicLength_MSB = chr((len(self.Topic) & 0xFF00) >> 8)
        self.TopicLength_LSB = chr(len(self.Topic) & 0x00FF)


    def fixed_header(self):
    
        header = self.message_type
        
        if self.DUP == 1: header = header or 0x08
        
        if self.QoS == 1: header = header or 0x02
        elif self.QoS == 2: header = header or 0x04
        elif self.QoS == 3: header = header or 0x06

        if self.retain == 1: header = header or 0x01

        return chr(header)
        
    def fixed_header_remaining_length(self):
        remaining_length = format_length(len(
            self.TopicLength_MSB + 
            self.TopicLength_LSB +
            self.Topic +
            self.Payload))
            
        return remaining_length
            
    def assemble(self):

        message = (self.fixed_header() +
                    self.fixed_header_remaining_length() +
                    self.TopicLength_MSB +
                    self.TopicLength_LSB +
                    self.Topic +           
                    self.Payload)    
                
        return message

#=========================================================================================

class Client(object):
    def __init__(self):
        self.sock = ''


    def connect(self,address="iot.eclipse.org", port=1883, keep_alive=60 ):
        # Create a socket connection to the server and connect to it
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Try connect to the socket
        self.sock.connect((address, port))

        # Send a CONNECT message
        self.sock.send(CONNECT(client_id = "someClientID", keep_alive=keep_alive).assemble())
        rsps = self.sock.recv(100)

        # Print the response message
        print(CONNACK().parse(response = rsps)[1])

        return

    def disconnect(self):

        self.sock.send(DISCONNECT().assemble())

        return

    def publish(self,topic = 'testtopic/subtopic', payload = 'Hello World!', qos = 0):

        self.sock.send(PUBLISH(topic = topic, payload = payload, qos = qos).assemble())

        return

#=========================================================================================

def format_length(length):
    remaining_length_string = ''
    while(length>0):
        digit = length % 128
        length = length / 128
        if(length>0):
            digit = digit | 0x80
        remaining_length_string = remaining_length_string + chr(digit)
    return remaining_length_string

#=========================================================================================

if __name__ == "__main__":


    MQTT_SERVER = "iot.eclipse.org"
    MQTT_PORT = 1883


    # Create a socket connection to the server and connect to it
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try connect to the socket
    s.connect((MQTT_SERVER, MQTT_PORT))

    # Send a CONNECT message
    s.send(CONNECT(client_id = "someClientID", keep_alive=1800).assemble())
    rsps = s.recv(100)

    # Print the response message
    print(CONNACK().parse(response = rsps)[1])

    # Send a PUBLISH message
    s.send(PUBLISH(topic = 'testtopic/subtopic', payload = 'Hello World!', qos = 0).assemble())

    # Send a DISCONNECT message
    s.send(DISCONNECT().assemble())
