import RPi.GPIO as GPIO
import logging
import os
from flask import Flask
from flask_ask import Ask, request, session, question, statement


GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def new_launch():
	return question('What would you like to do?')

@ask.intent('GPIOControlIntent', convert={'status': string , 'pin': int})
def gpio_control(status, pin):
    try:
        pinNum = int(pin)
    except Exception as e:
        return statement('Pin number not valid.')
	pinList = [8,7]
	if pinNum not in pinList:
		return statement('Pin is unused')
    GPIO.setup(pinNum, GPIO.OUT)

    if status in ['on', 'high']:    GPIO.output(pinNum, GPIO.HIGH)
    if status in ['off', 'low']:    GPIO.output(pinNum, GPIO.LOW)

    return statement('Turning pin {} {}'.format(pin, status))
	
if __name__ == '__main__':
    app.run(debug=True)