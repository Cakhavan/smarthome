


from gpiozero import Button, LED
from time import sleep
 
#--------------------------------------------#








#------------Sensor Declarations-------------#
#lamp is connected to GPIO4 as an LED
lamp = LED(17)




while True:
	lamp.on()
	sleep(3)
	lamp.off()
	sleep(3)
#	if flag == 1:
#		lamp.on()
#	else:
#		lamp.off()

#	while door_sensor.is_held:

#		doorCount = doorCount + 1
#		door = "door has been opened: " + str(doorCount) + "times"
#		pubnub.publish().channel('ch1').message(door).async(publish_callback)


#	door = "door is closed"
#	pubnub.publish().channel('ch1').message(door).async(publish_callback)


#	while light.is_held:
#		pubnub.publish().channel('ch1').message("lights are on").async(publish_callback)

#	pubnub.publish().channel('ch1').message("lights are off").async(publish_callback)
#
	


