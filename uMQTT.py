# Message types (subset of MQTT 3.1)
CONNECT = 0x10
PUBLISH = 0x30
SUBSCRIBE = 0x80
UNSUBSCRIBE = 0xA0
DISCONNECT = 0xE0

#=========================================================================================


class connect(object):

    def __init__(self, clientID):
        self.clientID = clientID
        
        self.MESSAGETYPE = CONNECT
        
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

class connack(object):

    def __init__(self):
    
        self.MESSAGETYPE = DISCONNECT
        
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

class disconnect(object):

    def __init__(self):
    
        self.MESSAGETYPE = DISCONNECT
        
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

class publish(object):

    def __init__(self, topic, payload, qos):
        self.Topic = topic
        self.Payload = payload
        self.QoS = qos
        
        self.MESSAGETYPE = PUBLISH
        
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