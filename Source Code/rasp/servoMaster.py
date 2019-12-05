import RPi.GPIO as GPIO
import time

servoPIN = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0) # Initialization

try:
  while True:
    p.ChangeDutyCycle(7.5)
    time.sleep(5)
    p.ChangeDutyCycle(12.5)
    time.sleep(5)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()