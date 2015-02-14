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

#   TODO
#=========================================================================================


import uMQTT as mqtt
import time


try:

    CM = mqtt.ClientManager()
    CM.create_client(client_id="bushveldlabs-Dev" , keep_alive=20, server="iot.eclipse.org", port=1883)

    CM.start()

    while True:
        # do some other stuff here

        # TODO add error handling when doing these publishes to make sure that the client id is actually in the list
        CM.client_directory['bushveldlabs-Dev'].publish(topic = 'testtopic/subtopic', payload = 'Hello World!', qos = 0)
        time.sleep(10) # Publish every 10 seconds


except(KeyboardInterrupt, SystemExit):
    print("Exiting")