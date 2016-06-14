###############################################################################
##                                                                           ##
##   raspiforce tennis                                                       ##
##   Use Raspberry Pi to simulate IoT sensor reading and automated case      ##
##   creation in Salesforce Service Cloud                                    ##
##   Based on the ADXL345 sensor for acceleration                            ##
##                                                                           ##
##   Use --simulation as commandline parameter to execute without            ##
##   Raspberry Pi connected and simulate asset and case creation             ##
##                                                                           ##
##   Use --chat as commandline parameter to publish status messages          ##
##   to the Websocket Chat server                                            ##
##                                                                           ##
##   See GitHub project for more details:                                    ##
##   https://github.com/tegeling/raspiforce                                  ##
##                                                                           ##
##   Thomas Egeling                                                          ##
##   tegeling@salesforce.com                                                 ##
##                                                                           ##
##   based on: ADXL345 Python example                                        ##
##   author:  Jonathan Williamson                                            ##
##   http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer    ##
##                                                                           ##
###############################################################################

from simple_salesforce import Salesforce
from websocket import create_connection
import json
import ConfigParser
import time
import os
import glob
import sys
import adxl345

#
# Define the celsius temperature threshold to raise alarms and create a new support case
# Set a default value that can be replaced by configuration settings in the setup Salesforce org
#
global alarm_threshold_default
alarm_threshold_default = 25

#
# Sleep in seconds to allow cooldown of the temperature
#
global sleep_reset
sleep_reset = 60

def print_msg():
	if chat_mode:
		print 'Program is running in chat mode...'
	if simulation_mode:
		print 'Program is running in simulation mode...'
	else:
		print 'Program is running'
		print 'Please press Ctrl+C to end the program...'


def destroy():   # When program ending, the function is executed. 
	if chat_mode:
		ws.close()
	print "Exit."

def chat(handle, msg):
	global ws
	#
	# Send new chat message to monitoring service via websockets
	#
	myText = u'{"handle": "' + handle + '","text": "' + msg + '"}'
	myjson = json.loads(myText)
	payload = json.dumps(myjson, ensure_ascii = False).encode('utf8')
	ws.send(payload)

def setup():
	#
	# Declare global variables
	#
	global myRegId
	global myUsername
	global myPassword
	global myToken
	global contactid
	global subject
	global ws
	global adxl

	#
	# setup Raspberry Pi ADXL345
	# see http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer
	#
	if not simulation_mode:
		adxl = adxl345.ADXL345()
		#adxl.setRange(adxl345.RANGE_2G)
		adxl.setRange(adxl345.RANGE_16G)

	#
	# Read configuration from file
	#
	config = ConfigParser.RawConfigParser()
	config.read('salesforce_login.cfg')

	#
	# Establish Websockt connection for monitoring chat service
	#
	if chat_mode:
		ws_url = config.get('Chat', 'ws_url')
		ws = create_connection(ws_url)


	#
	# Lookup Salesforce demo org credentials and configuration
	#
	sf_lookup = Salesforce(username=config.get('Salesforce', 'username'), password=config.get('Salesforce', 'password'), security_token=config.get('Salesforce', 'security_token'))
	result = sf_lookup.query("SELECT Id, Username__c, Password__c, Security_Token__c, Case_Contact_Id__c, Case_Subject__c FROM Raspberry_Pi_Demo__c WHERE Active__c = true")

	#
	# Register new demo run
	#
	myRegId = result.get('records')[0].get('Id')	
	sf_lookup.Raspberry_Pi_Demo_Registration__c.create({'Raspberry_Pi_Demo__c':myRegId,'Status__c':'connected'})

	myUsername = result.get('records')[0].get('Username__c')
	myPassword =  result.get('records')[0].get('Password__c')
	myToken = result.get('records')[0].get('Security_Token__c')

	contactid = result.get('records')[0].get('Case_Contact_Id__c')
	subject = result.get('records')[0].get('Case_Subject__c')

	if chat_mode:
		chat("Sensor","Connection established.")

def loop():
	#
	# Create new connection to demo org
	#
	sf = Salesforce(username=myUsername, password=myPassword, security_token=myToken)

	##
	## Infinite loop to allow sensor reading
	##
	global adxl
	while True and not simulation_mode:
		#
		# Loop the device and check the sensor
		#
		alarm = False
		while not alarm:
			axes = adxl.getAxes(True)
			abs_x = abs(axes['x'])
			abs_y = abs(axes['y'])
			abs_z = abs(axes['z'])
			if (abs_x > 10):
				#print "   x = %.3fG" % ( axes['x'] )
				#print "   y = %.3fG" % ( axes['y'] )
				#print "   z = %.3fG" % ( axes['z'] )
				if chat_mode:
					chat("Sensor", "HAMMER SLAMMER")
				print "You are the HAMMER SLAMMER!!!"
				time.sleep(2)
				alarm = True
				break
			if (abs_x > 6):
				print "Medium shot"
				if chat_mode:
					chat("Sensor", "Medium shot")
				time.sleep(2)
			if (abs_x > 4):
				print "Low shot"
				if chat_mode:
					chat("Sensor", "Low shot")
				time.sleep(2)
		#
		# Create new interaction record
		#
		sf.RaspiInteraction__c.create({'Msg__c':subject,'Contact__c':contactid})

		if chat_mode:
			chat("Sensor", "Interaction created.")

	#
	# Simulate new interaction 
	#
	if simulation_mode:
		sf.RaspiInteraction__c.create({'Msg__c':subject,'Contact__c':contactid})
		if chat_mode:
			chat("Sensor", "Interaction simulated.")

if __name__ == '__main__': # Program starting from here 
	global simulation_mode
	global chat_mode
	simulation_mode = False
	chat_mode = False
	global ws

	if (len(sys.argv) == 2) and (str(sys.argv[1]) == "--simulation"):
		simulation_mode = True
	if (len(sys.argv) == 2) and (str(sys.argv[1]) == "--chat"):
		chat_mode = True
	if (len(sys.argv) == 3) and (str(sys.argv[1]) == "--simulation") and (str(sys.argv[2]) == "--chat"):
		chat_mode = True
		simulation_mode = True
	if (len(sys.argv) == 3) and (str(sys.argv[1]) == "--chat") and (str(sys.argv[2]) == "--simulation"):
		chat_mode = True
		simulation_mode = True
	print_msg()
	setup() 
	try:
		loop()
	except KeyboardInterrupt:  
		destroy()  

