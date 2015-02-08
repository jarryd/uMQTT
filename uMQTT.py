# Message types (subset of MQTT 3.1)
MSG_CONNECT = 0x10
MSG_CONNACK = 0x20
MSG_PUBLISH = 0x30
MSG_SUBSCRIBE = 0x80
MSG_UNSUBSCRIBE = 0xA0
MSG_DISCONNECT = 0xE0

#=========================================================================================


class CONNECT(object):

    def __init__(self, clientID):
        self.clientID = clientID
        
        self.MESSAGETYPE = MSG_CONNECT
        
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
        
        self.PROTOCOLNAME = "MQIsdp"
        self.PROTOCOLVERSION = chr(3)
        self.KEEPALIVE = 60
        
        # Client ID length
        self.clientIDlength_MSB = chr((len(self.clientID) & 0xFF00) >> 8)
        self.clientIDlength_LSB = chr((len(self.clientID) & 0x00FF)) 
        
        # Protocol name length
        self.PROTOCOLNAMElength_MSB = chr((len(self.PROTOCOLNAME) & 0xFF00) >> 8)
        self.PROTOCOLNAMElength_LSB = chr(len(self.PROTOCOLNAME) & 0x00FF)
        
        # Keepalive 
        self.KEEPALIVE_MSB = chr((self.KEEPALIVE & 0xFF00) >> 8)
        self.KEEPALIVE_LSB = chr(self.KEEPALIVE & 0x00FF)
        

    def ConnectFlags(self):
    
        CONNECTFLAGS = 0x00
        
        if self.User_name_flag: CONNECTFLAGS = CONNECTFLAGS | 0x80
        if self.Password_flag: CONNECTFLAGS = CONNECTFLAGS | 0x40
        if self.Will_RETAIN: CONNECTFLAGS = CONNECTFLAGS | 0x20
        if self.Will_QoS_MSB: CONNECTFLAGS = CONNECTFLAGS | 0x10
        if self.Will_QoS_LSB: CONNECTFLAGS = CONNECTFLAGS | 0x08
        if self.Will_flag: CONNECTFLAGS = CONNECTFLAGS | 0x04
        if self.Clean_Session: CONNECTFLAGS = CONNECTFLAGS | 0x02
        
        return chr(CONNECTFLAGS)

    def FixedHeader(self):
    
        FIXEDHEADER = self.MESSAGETYPE
        
        if self.DUP == 1: FIXEDHEADER = FIXEDHEADER | 0x08
        
        if self.QoS == 1: FIXEDHEADER = FIXEDHEADER | 0x02
        elif self.QoS == 2: FIXEDHEADER = FIXEDHEADER | 0x04
        elif self.QoS == 3: FIXEDHEADER = FIXEDHEADER | 0x06

        if self.retain == 1: FIXEDHEADER = chr(FIXEDHEADER) | 0x01

        return chr(FIXEDHEADER)
        
    def FixedHeaderRemainingLength(self):
        REMAININGLENGTH = FormatLength(len(
            self.PROTOCOLNAMElength_MSB + 
            self.PROTOCOLNAMElength_LSB +
            self.PROTOCOLNAME +
            self.PROTOCOLVERSION +
            self.ConnectFlags() +
            self.KEEPALIVE_MSB +
            self.KEEPALIVE_LSB +
            self.clientIDlength_MSB +
            self.clientIDlength_LSB +
            self.clientID))
            
        return REMAININGLENGTH
            
    def Assemble(self):

        message = (self.FixedHeader() +
                    self.FixedHeaderRemainingLength() +
                    self.PROTOCOLNAMElength_MSB +
                    self.PROTOCOLNAMElength_LSB +
                    self.PROTOCOLNAME +
                    self.PROTOCOLVERSION +
                    self.ConnectFlags() +
                    self.KEEPALIVE_MSB +
                    self.KEEPALIVE_LSB +
                    self.clientIDlength_MSB +
                    self.clientIDlength_LSB +
                    self.clientID)      
                
        return message

#-----------------------------------------------------------------------------------------

class CONNACK(object):

    def __init__(self):
        self.MESSAGETYPE = MSG_CONNACK
        self.REMAININGLENGTH = 0
        
        self.return_codes = {0: 'Connection Accepted',
                             1: 'Connection Refused: unacceptable protocol version',
                             2: 'Connection Refused: identifier rejected',
                             3: 'Connection Refused: server unavailable',
                             4: 'Connection Refused: bad user name or password',
                             5: 'Connection Refused: not authorized'}

    def Parse(self, response):
        """ Parse CONNACK message"""
        
        if len(response) == 4:
            """ Check that the response is the expected size (should be 2 fixed header bytes
            and 2 variable header bytes)"""
        
            # Convert the hex length byte to an integer
            self.REMAININGLENGTH = ord(response[1])
            
            code = ord(response[3])
            
            message = self.return_codes[ord(response[3])]
            
        else:
            # Something is wrong...
            code = ''
            message = ''
            print("ERROR: Something is wrong in the CONNACK parser. Didn't recieve the correct response size")

        return code, message

#-----------------------------------------------------------------------------------------

class DISCONNECT(object):

    def __init__(self):
    
        self.MESSAGETYPE = MSG_DISCONNECT
        
        self.DUP = 0
        self.QoS = 0
        self.retain = 0

    def FixedHeader(self):
    
        FIXEDHEADER = self.MESSAGETYPE
        
        if self.DUP == 1: FIXEDHEADER = FIXEDHEADER | 0x08
        
        if self.QoS == 1: FIXEDHEADER = FIXEDHEADER | 0x02
        elif self.QoS == 2: FIXEDHEADER = FIXEDHEADER | 0x04
        elif self.QoS == 3: FIXEDHEADER = FIXEDHEADER | 0x06

        if self.retain == 1: FIXEDHEADER = FIXEDHEADER | 0x01

        return chr(FIXEDHEADER)

    def Assemble(self):

        message = (self.FixedHeader() + "\x00")
                
        return message


#-----------------------------------------------------------------------------------------

class PUBLISH(object):

    def __init__(self, topic, payload, qos):
        self.Topic = topic
        self.Payload = payload
        self.QoS = qos
        
        self.MESSAGETYPE = MSG_PUBLISH
        
        self.DUP = 0
        self.QoS = 0
        self.retain = 0         

        self.TopicLength_MSB = chr((len(self.Topic) & 0xFF00) >> 8)
        self.TopicLength_LSB = chr(len(self.Topic) & 0x00FF)


    def FixedHeader(self):
    
        FIXEDHEADER = self.MESSAGETYPE
        
        if self.DUP == 1: FIXEDHEADER = FIXEDHEADER | 0x08
        
        if self.QoS == 1: FIXEDHEADER = FIXEDHEADER | 0x02
        elif self.QoS == 2: FIXEDHEADER = FIXEDHEADER | 0x04
        elif self.QoS == 3: FIXEDHEADER = FIXEDHEADER | 0x06

        if self.retain == 1: FIXEDHEADER = FIXEDHEADER | 0x01

        return chr(FIXEDHEADER)
        
    def FixedHeaderRemainingLength(self):
        REMAININGLENGTH = FormatLength(len(
            self.TopicLength_MSB + 
            self.TopicLength_LSB +
            self.Topic +
            self.Payload))
            
        return REMAININGLENGTH
            
    def Assemble(self):

        message = (self.FixedHeader() +
                    self.FixedHeaderRemainingLength() +
                    self.TopicLength_MSB +
                    self.TopicLength_LSB +
                    self.Topic +           
                    self.Payload)    
                
        return message


#-----------------------------------------------------------------------------------------

def FormatLength(length):
    remaining_length_string = ''
    while(length>0):
        digit = length % 128
        length = length / 128
        if(length>0):
            digit = digit | 0x80
        remaining_length_string = remaining_length_string + chr(digit)
    return remaining_length_string