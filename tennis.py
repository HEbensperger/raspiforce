# ADXL345 Python example 
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
# 
# This is an example to show you how to use our ADXL345 Python library
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

import adxl345
import time
  
adxl = adxl345.ADXL345()
#adxl.setRange(adxl345.RANGE_2G)
adxl.setRange(adxl345.RANGE_16G)

while True:
	axes = adxl.getAxes(True)
	abs_x = abs(axes['x'])
	abs_y = abs(axes['y'])
	abs_z = abs(axes['z'])
	if (abs_x > 10):
		#print "   x = %.3fG" % ( axes['x'] )
		#print "   y = %.3fG" % ( axes['y'] )
		#print "   z = %.3fG" % ( axes['z'] )
		print "You are the HAMMER SLAMMER!!!"
		break
	#time.sleep(1)
	if (abs_x > 6):
		print "Medium shot"
	if (abs_x > 4):
		print "Low shot"
