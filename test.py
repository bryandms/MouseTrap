#!/usr/bin/python

# Credits: Mario Perez Esteso
# References: https://geekytheory.com/tutorial-raspberry-pi-uso-de-picamera-con-python/

import time
import picamera
import smtplib
import RPi.GPIO
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
from email.Encoders import encode_base64

RPi.GPIO.setmode( RPi.GPIO.BCM )
RPi.GPIO.setup( 11, RPi.GPIO.IN, pull_up_down = RPi.GPIO.PUD_UP )

#===================================================================
#   SENSOR TEST
#===================================================================
while True:
	if RPi.GPIO.input( 2 ) == RPi.GPIO.LOW:
		print(" active ")
		with picamera.PiCamera() as picam:
	    		picam.start_preview()
	    		time.sleep( 5 )
	    		picam.stop_preview()
		    	picam.close()
			break
RPi.GPIO.cleanup()
		

#===================================================================
#	PREVIEW
#===================================================================

with picamera.PiCamera() as picam:
    picam.start_preview()
    time.sleep(5)
    picam.stop_preview()
    picam.close()


#===================================================================
#	TAKE A PHOTO
# png, gif, bmp, yuv, rgb y raw
#===================================================================

with picamera.PiCamera() as picam:
    picam.start_preview()
    time.sleep( 1 )
    picam.capture('name.jpg')
    picam.stop_preview()
    picam.close()

#===================================================================
#	SHOOT A VIDEO
#===================================================================

with picamera.PiCamera() as picam:
    picam.start_preview()
    picam.start_recording( 'video.h264' )
    picam.wait_recording( 3 )
    picam.stop_recording()
    picam.stop_preview()
    picam.close()

#===================================================================
#	ADJUSTMENT OF RESOLUTION
#===================================================================

with picamera.PiCamera() as picam:
    picam.resolution = ( 2592, 1944 )
    picam.start_preview()
    time.sleep( 3 )
    picam.capture( 'photo.jpg' )
    picam.capture( 'photo.jpg', resize = ( 1024,768 ) )
    picam.stop_preview()
    picam.close()

#===================================================================
#	BRIGHTNESS
#===================================================================

with picamera.PiCamera() as picam:
    picam.start_preview()
    picam.brightness = 60
    picam.ISO = 100 
    time.sleep( 3 ) 
    picam.shutter_speed = 300000 
    picam.capture('photo.jpg', resize = ( 1024,768 ) ) 
    picam.stop_preview()
    picam.close()

#===================================================================
#	IMAGE EFFECTS
# 'negative', 'solarize', 'gpen'
#===================================================================

with picamera.PiCamera() as picam:
    picam.led = False
    picam.start_preview()
    picam.image_effect = 'negative'
    time.sleep(5)
    picam.stop_preview()
    picam.close()

#===================================================================
#	EMAIL WITH IMAGE
#================================================================== """

msg = MIMEMultipart()
msg['From'] = "your_email"
msg['To'] = "your_destiny"
msg['Subject'] = "MouseTrap"

file = open( "name.jpg", "rb" )
attach_image = MIMEImage( file.read() )
msg.attach( MIMEText( "Already you have dinner tonight! He has caught a mouse." ) )
msg.attach( attach_image )

mailServer = smtplib.SMTP( 'smtp.gmail.com', 587 )
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login( "your_email", "your_password" )

mailServer.sendmail( "your_email", "your_destiny", msg.as_string() )
mailServer.close()