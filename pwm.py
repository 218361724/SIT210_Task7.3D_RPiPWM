# PWM with Rasberry Pi

# Demonstrate working with PWM by measuring distance to an approaching
# object and using that to control buzzer pitch

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
 
# Setup GPIO pins
usonicTriggerPin = 19
usonicEchoPin = 26
buzzerPin = 13
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.setup(usonicTriggerPin, GPIO.OUT)
GPIO.setup(usonicEchoPin, GPIO.IN)

# Setup PWM buzzer
buzzerPwm = GPIO.PWM(buzzerPin, 1000)
buzzerPwm.start(0)

def getDistToObj():
    GPIO.output(usonicTriggerPin, GPIO.HIGH)
    time.sleep(0.01 / 1000) # 0.01ms
    GPIO.output(usonicTriggerPin, GPIO.LOW)
 
    startTime = time.time()
    stopTime = time.time()
 
    while GPIO.input(usonicEchoPin) == 0:
        startTime = time.time()
 
    while GPIO.input(usonicEchoPin) == 1:
        stopTime = time.time()
 
    secondsElasped = stopTime - startTime

    # Get distance by multiplying time diff by the speed of sound (in cm per second)
    # then dividing by 2 since we need to go to the object and back
    distance = (secondsElasped * 34300) / 2
 
    return distance
 
try:
    while True:
        distToObj = getDistToObj()

        if (distToObj < 50):
            # Increase pitch as object gets closer
            buzzerPwm.ChangeDutyCycle(100 - (distToObj * 2))
        else:
            # Turn buzzer off when no object is detected
            buzzerPwm.ChangeDutyCycle(0)

        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
