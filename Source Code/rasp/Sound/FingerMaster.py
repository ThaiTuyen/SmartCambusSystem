#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

import time
from pyfingerprint.pyfingerprint import PyFingerprint
import lcddriver

from threading import Thread
import _thread
import const as CONST
from pygame import mixer
import RPi.GPIO as GPIO

import time



GPIO.setwarnings(False)
PinAddFinger = 5
servoPIN = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(PinAddFinger, GPIO.IN)

GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization
p.ChangeDutyCycle(12.5)
display = lcddriver.lcd()
mixer.init()
try:
	soundWarning = mixer.Sound('/home/pi/FinalProject/FactoryGuard/Sound/warning.wav')
	soundCorect = mixer.Sound('/home/pi/FinalProject/FactoryGuard/Sound/corectBeat.wav')
	soundUnCorect = mixer.Sound('/home/pi/FinalProject/FactoryGuard/Sound/uncorectBeat.wav')
except:
	print("enor load sound")

## Enrolls new finger
##

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')
except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to enroll new finger
def addFinger():
    try:
        print('Waiting for finger...')
        display.lcd_clear()
        display.lcd_display_string("Add finger", 1)
        display.lcd_display_string("push In finger", 2)
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]
        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            display.lcd_clear()
            display.lcd_display_string("Finger already!", 1)
            time.sleep(1)
            return False
        print('Push Out finger...')
        display.lcd_clear()
        display.lcd_display_string("Push Out finger", 2)
        time.sleep(2)
        display.lcd_clear()
        display.lcd_display_string("keep touch", 1)
        print('Waiting for  finger again...')
        
        ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass
            ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)
        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')
            display.lcd_clear()
            display.lcd_display_string("Error", 1)            
            
        ## Creates a template
        f.createTemplate()
        
        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        display.lcd_clear()
        display.lcd_display_string("successfully!", 1)
        display.lcd_display_string('position #' + str(positionNumber), 2)
        return True
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        display.lcd_clear()
        display.lcd_display_string("Error", 1)  
        return False
        
        

def checkFinger():
    while 1:
        try:
            print('Waiting for finger...')
            display.lcd_clear()
            display.lcd_display_string("Check finger", 1)
            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass
            ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(0x01)
            
            ## Searchs template
            result = f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            if ( positionNumber == -1 ):
                print('No match found!')
                display.lcd_clear()
                display.lcd_display_string("No match found!", 1)
                try:
                	soundUnCorect.play()
                except:
                	print("not play sound")
                time.sleep(2)
  
            else:
                CONST.PositionNum = positionNumber
                print('Found template at position #' + str(positionNumber))
                display.lcd_clear()
                display.lcd_display_string("Wellcome!", 1)
                display.lcd_display_string(' At position #' + str(positionNumber), 2)
                if positionNumber == 0 and checkButon() == True:
                    while checkButon() == True:
                        display.lcd_clear()
                        display.lcd_display_string("Add finger", 2)
                        display.lcd_display_string("OK config done", 1)
                        time.sleep(1)
                    while True:
                        addFinger() 
                        time.sleep(2)
                        display.lcd_clear()
                        display.lcd_display_string("Wait for Again", 1)
                        display.lcd_display_string("Button for exit", 2)
                        time.sleep(2)
                        if checkButon() == True:
                            break
                else:
                   CONST.DataCheckIn[0] = CONST.DataCheckIn[0] +1;
                   CONST.PositionAccess = True
                   ServoMaster()
                   
                try:
                	soundCorect.play()
                except:
                	print("not play sound")

                #time.sleep(2)
        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))

def checkButon():
    if GPIO.input(PinAddFinger) == False:
        return True
    else:
        return False

def ClearAllFinger():
    try:
        print("Clear All Finger")
        return True

    except:
        print("Don't working clear, try again")
        return False


def FingerMaster_Begin():
    try:
        _thread.start_new_thread(Checkin.checkFinger, ())
    except:
        print("don't opent finger")

def ServoMaster():
	try:
		p.ChangeDutyCycle(7.0)
		time.sleep(5)
		p.ChangeDutyCycle(12.5)
		time.sleep(0.5)
	except KeyboardInterrupt:
		p.ChangeDutyCycle(12.5)
		time.sleep(0.5)
		p.stop()
		GPIO.cleanup()

#addFinger()
#checkFinger()
