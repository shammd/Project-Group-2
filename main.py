#!/usr/bin/env pybricks-micropython
"""
Example LEGO® MINDSTORMS® EV3 Robot Arm Program
----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait
import time 

# Initialize the EV3 Brick
ev3 = EV3Brick()

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.A)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation
# of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it. We would like positive speed values
# to make the arm go away from the Touch Sensor. This corresponds
# to counterclockwise rotation of the motor.
base_motor= Motor(Port.C, Direction.COUNTERCLOCKWISE, [12,36])


# Limit the elbow and base accelerations. This results in
# very smooth motion. Like an industrial robot.
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the elbow
# is in the starting position. This is when the sensor sees the
# white beam up close.
color_sensor = ColorSensor(Port.S2)

""" Code starts here """

# Define förinställda positioner i grader relativt till zero point
POSITIONS = {
    1: -100, # 
    2: 0,    # zero point
    3: 47,   # ungefär 45° från andra position (135° från zero point) - drop off zone för gröna objekt
    4: 90,   # ungefär 45° från tredje position (180° från zero point)
    5: -51   # Extra postion sido led 
} 

COLOR_LST = [Color.RED, Color.GREEN, Color.YELLOW]

P1 = []
P2 = []
P3 = [Color.RED, Color.GREEN]
P4 = [Color.YELLOW]
P5 = []

# Function to close the gripper
def close_gripper():
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=35)
    print('close')

# Function to open the gripper
def open_gripper():
    gripper_motor.run_target(150, -90)
    #gripper_motor.run_until_stalled(-200, then=Stop.HOLD, duty_limit=7)
    print('open')

# Function to move the elbow upward
def elbow_up(degree):
    elbow_motor.run_angle(60,degree)

# Function to move the elbow downward
def elbow_down(degree):
    elbow_motor.run_angle(60,-degree)

# Funktion för att detektera färg
def detect_color():
    # Läs färgen från färgsensorn
    detected_color = color_sensor.color()
    print(detected_color)
    return detected_color

# Funktion för att uttala färgens namn
def announce_color(color):
    if color == Color.RED:
        ev3.speaker.say("Red")
    elif color == Color.GREEN:
        ev3.speaker.say("Green")
    elif color == Color.YELLOW:
        ev3.speaker.say("Yellow")
    elif color == Color.BLUE:
        ev3.speaker.say("Blue")
    elif color == None:
        ev3.speaker.say('No item found')

            
def item_zone(position):
    target_position = POSITIONS.get(position)
    if target_position is None:
        print("Ogiltig position!")
        return

    current_angle = base_motor.angle()
    delta_angle = target_position - current_angle

    # Roterar armen till den förinställda positionen
    base_motor.run_angle(60, delta_angle)

def elevated_position(position):
    item_zone(position)
    item_color = detect_color()
    if item_color in COLOR_LST:
        open_gripper()
        elbow_down(55)
        close_gripper()
    return item_color

def reset_robot():
    while not base_switch.pressed():
        base_motor.run(-60)
    base_motor.run_angle(60,110)
    base_motor.reset_angle(0)   

def pick_item(position):
    item_zone(position) 
    elbow_down(90)
    close_gripper()
    elbow_up(45)

def drop_item(position):
    elbow_up(45)
    item_zone(position)
    elbow_down(90)
    open_gripper()
    elbow_up(90)

def sort_item_by_time():
    pick_item(1)
    item_color = detect_color()
    if item_color in COLOR_LST:
        drop_item(3)
    else: reset_robot()

def sort_objects_for_time(duration):
    start_time = time.time()  # Hämta starttiden
    while time.time() - start_time < duration:  # Utför sortering under angiven tid
        ev3.speaker.say('Start')

def NoItemFound():
    elbow_up(45) 
    open_gripper()
    
def reset_arm(open_, up_90):
    if open_ == 0:
        open_gripper()
    elif open_ == 1:
        pass
    elif open_ == 2:
        close_gripper()
    
    if up_90 == 90:
        pass
    elif up_90 == 0:
        elbow_up(90)


def main():
    open_gripper()
    elbow_up(90)
    reset_robot()
    while True:
        pick_item(1)
        item_C = detect_color()
        announce_color(item_C)
        if item_C == Color.RED:
            drop_item(3)
        elif item_C == Color.GREEN: 
            drop_item(3)
        elif item_C == Color.YELLOW:
            drop_item(4)
        else: 
            NoItemFound()
            continue

def R_main():
    reset_arm()
    reset_robot()
    L_P = False 
    while not L_P:
        count = 0
        pick_item(1)
        item_C = detect_color()
        announce_color(item_C)
        if item_C in P3:
            drop_item(3)
        elif item_C in P4:
            drop_item(4)
        elif item not in COLOR_LST: 
            NoItemFound()
            count += 1
        itemC = elevated_position(2)
        announce_color(itemC)
        if itemC in P3:
            drop_item(3)
        elif itemC in P4:
            drop_item(4)
        elif itemC not in COLOR_LST: 
            continue
            count += 1
        
        if count == 20:
            L_P = True

if __name__ == "__main__":
    main()
    
