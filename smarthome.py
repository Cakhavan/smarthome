

#---------------Library Setup----------------#
import pubnub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory


from gpiozero import Button, LED
from time import sleep
 
#--------------------------------------------#




#----------------PubNub Setup----------------#
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-1575c412-2116-11e8-a7d0-2e884fd949d2"
pnconfig.publish_key = "pub-c-2d8f55f6-daa7-467b-923b-6a1e6570c9fc"
pnconfig.ssl = False
pubnub = PubNub(pnconfig)
#--------------------------------------------#





#------------Sensor Declarations-------------#
#lamp is connected to GPIO4 as an LED
lamp = LED(4)

#door sensor is connected to GPIO3 as a Button
door_sensor = Button(3)

#light sensor is connected to GPIO14 as a Button
light = Button(14)
#--------------------------------------------#



#door counter
doorCount = 0



class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass
        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if status.operation == PNOperationType.PNSubscribeOperation \
                or status.operation == PNOperationType.PNUnsubscribeOperation:
            if status.category == PNStatusCategory.PNConnectedCategory:
                pass
                # This is expected for a subscribe, this means there is no error or issue whatsoever
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                pass
                # This usually occurs if subscribe temporarily fails but reconnects. This means
                # there was an error but there is no longer any issue
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                pass
                # This is the expected category for an unsubscribe. This means there
                # was no error in unsubscribing from everything
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                pass
                # This is usually an issue with the internet connection, this is an error, handle
                # appropriately retry will be called automatically
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # This means that PAM does allow this client to subscribe to this
                # channel and channel group configuration. This is another explicit error
            else:
                pass
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult <link to the PNCONFIGURATION heartbeart config>
            if status.is_error():
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            pass
            # Encountered unknown status type

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def message(self, pubnub, message):
        if message.message == 'ON':
        	lamp.on()
        	pubnub.publish().channel('ch1').message("lamp has been turned on").async(publish_callback)
        	sleep(3)
        elif message.message == 'OFF':
        	lamp.off()
        	pubnub.publish().channel('ch1').message("lamp has been turned off").async(publish_callback)



 
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('ch1').execute()


def publish_callback(result, status):
    pass
    # Handle PNPublishResult and PNStatus
 


while True:

	while door_sensor.is_held:

		doorCount = doorCount + 1
		door = "door has been opened: " + str(doorCount) + "times"
		pubnub.publish().channel('ch1').message(door).async(publish_callback)


	door = "door is closed"
	pubnub.publish().channel('ch1').message(door).async(publish_callback)


	while light.is_held:
		pubnub.publish().channel('ch2').message("lights are on").async(publish_callback)

	pubnub.publish().channel('ch2').message("lights are off").async(publish_callback)

	sleep(3)


