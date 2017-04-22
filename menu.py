#!/usr/bin/python
import os
import time
import picamera
import smtplib
import RPi.GPIO
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
from email.Encoders import encode_base64

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(17, RPi.GPIO.IN)
RPi.GPIO.setup(27, RPi.GPIO.OUT)
motor = RPi.GPIO.PWM(27, 50)

# -------------- Mail --------------
def send_mail(email, extension):
	msg             = MIMEMultipart()
	msg['From']     = "no-reply@pmousetrap.com"
	msg['To']       = email
	msg['Subject']  = "MouseTrap"
 
    file            = open( extension, "rb" )
    attach_image    = MIMEImage( file.read() )
    attach_image.add_header( 'Content-Disposition', 'attachment; filename = ' + extension )
    msg.attach( MIMEText(" Already you have dinner tonight! He has caught a mouse. ") )
    msg.attach( attach_image )
 
    mailServer = smtplib.SMTP( 'smtp.gmail.com', 587 )
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login( "mail", "password" )
    mailServer.sendmail( "no-reply@pmousetrap.com", email, msg.as_string() )
    mailServer.close()

print "==============================================="
print "MouseTrap"
print "==============================================="

# ------------ Extension ------------
extension = raw_input(" Extensions: \t1. png \t2. gif \t3. bmp \nSelect an extension>> ")

if extension == "1":
	extension = ".png"
elif extension == "2":
	extension = ".gif"
elif extension == "3":
	extension = ".bmp"
else:
	print "It has a taken a picture with the default extension (.png)"
	extension = ".png"

extension = 'mouse' + extension

# ------------- Effects -------------
effect = raw_input(" Effects: \t1. Negative \t2. Solarize \t3. Gpen \nSelect an effect: ")
	
if effect == "1":
	effect = "negative"
elif effect == "2":
	effect = "solarize"
elif effect == "3":
	effect = "gpen"
else:
	effect = "none"

# ----------- Brightness ------------
num = raw_input(" Enter a number from 1 to 100 >> ")

if num < "0" or num > "100":
	num = "60"

with picamera.PiCamera() as picam:
	picam.image_effect = effect
	picam.brightness= int( num )

# ---------- Mouse capture ----------
while True:

	input_state = RPi.GPIO.input( 17 )
	
	if input_state == False:
		print(" active ")
		motor.start( 90 )

		for i in range( 0, 101, 5 ):
			motor.ChangeDutyCycle( i )
			time.sleep( 0.1 )

		for i in range( 100, -1, -5 ):
			motor.ChangeDutyCycle( i )
			time.sleep( 0.1 )
 
		with picamera.PiCamera() as picam:
	        	extension = 'mouse' + extension
        		picam.capture( extension )
        		picam.close()
			print(" Sending mail ")
			send_mail( 'Receiver mail', extension )
				
			break

	print(" waiting ")
motor.stop()