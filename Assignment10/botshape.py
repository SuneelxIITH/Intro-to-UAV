from __future__ import print_function

from dronekit import connect, VehicleMode, Command, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time, sys, argparse, math
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import time

import argparse  
#import Adafruit_MCP4725
import RPi.GPIO as GPIO
GPIO.cleanup

Motor_A_Pin1  = 29
Motor_A_Pin2  = 31
Motor_B_Pin1  = 38
Motor_B_Pin2  = 40

Motor_A_EN    = 32
Motor_B_EN    = 36

pwm_A = 0
pwm_B = 0

def setup():
    global pwm_A, pwm_B
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    
    
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)
    GPIO.setup(Motor_B_Pin1, GPIO.OUT)
    GPIO.setup(Motor_B_Pin2, GPIO.OUT)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    try:
        pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        pwm_B = GPIO.PWM(Motor_B_EN, 1000)
    except:
        pass
    
    
def motorStop():#Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)

def right():#Motor 2 positive and negative rotation
    global  pwm_B
    #if status == 0: # stop
        #motorStop()
    #else:
        #if direction == Dir_forward:
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.HIGH)
    time.sleep(0.1)
    stop()
    

def left():# Motor 1 positive and negative rotation
    global pwm_A
    #if status == 0: # stop
    #    motorStop()
    #else:
    #    if direction == Dir_forward:#
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.HIGH)
    time.sleep(0.1)
    stop()
    

def move():#Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.HIGH)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.HIGH)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)
    time.sleep(0.4)
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    time.sleep(0.1)



def stop():#Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)



print("Started:")
#print(Jetson.GPIO.VERSION)
setup()

connection_string = "/dev/ttyACM0"
print("\nConnecting to vehicle on: %s" % connection_string)

vehicle = connect(connection_string, wait_ready=True)

vehicle.wait_ready('autopilot_version')

print("\nGet vehicle attribute values:")
print(" Autopilot Firmware version: %s" % vehicle.version)
print(" Autopilot capabilities")
print("   Supports onboard compass calibration: %s" % vehicle.capabilities.compass_calibration)
print(" Global Location: %s" % vehicle.location.global_frame)
print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
print(" Local Location: %s" % vehicle.location.local_frame)
print(" GPS: %s" % vehicle.gps_0)
print(" EKF OK?: %s" % vehicle.ekf_ok)
print(" Heading: %s" % vehicle.heading)
print(" Groundspeed: %s" % vehicle.groundspeed)    # settable
print(" Heading: %s" % vehicle.heading)





#


bearing = 0
left()
time.sleep(2)



i=0
Required_Bearing = 0
while True:
    
    
    Current_Bearing = vehicle.heading
    bearing_diff = Current_Bearing - Required_Bearing
    
    
    if bearing_diff < -180:
        bearing_diff = (bearing_diff+360)
        print("             changed bearing_diff: ", bearing_diff)

    if bearing_diff > 180:
        bearing_diff = bearing_diff-360
        print("             changed bearing_diff: ", bearing_diff)


    
    print(" Heading: %s" % vehicle.heading)
    
    if bearing_diff < -3:
        right()
        time.sleep(0.5)
    elif bearing_diff > 3:
        left()
        time.sleep(0.5)
    else:
        if i < 6:
            move()
            i=i+1
        else:
            i=0
            Required_Bearing = Required_Bearing + 90
            if Required_Bearing == 360:
                Required_Bearing = 0
            #break


stop()

cmds = vehicle.commands
cmds.download()
cmds.wait_ready()

print("Finished")

#Close vehicle object before exiting script
print("\nClose vehicle object")
vehicle.close()
