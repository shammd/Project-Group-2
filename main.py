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
from pybricks.parameters import Port, Stop, Direction, Color, Button
from pybricks.tools import wait

ev3 = EV3Brick()

gripper_motor = Motor(Port.A)

arm_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

base_motor= Motor(Port.C, Direction.COUNTERCLOCKWISE, [12,36])

MAX_SPEED = 200
MAX_ACCELERATION = 120
arm_motor.control.limits(MAX_SPEED, MAX_ACCELERATION)
base_motor.control.limits(MAX_SPEED, MAX_ACCELERATION)

base_switch = TouchSensor(Port.S1)

color_sensor = ColorSensor(Port.S2)

""" Code starts here """

# To difine positions for pick up, elevated and drop zone
POSITIONS = {}

# Level of arm to move
ARM_LEVEL = {'down':0, 'ColorSensor':0, 'up':0}

COLOR_LST = ['Red','Blue','Green','Yellow']

# To close the gripper
def close_gripper():
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)

# To open the gripper
def open_gripper():
    gripper_motor.run_target(150, 0)

# To reset base robot: Angle 0 = middel, positive angle = left side, negative angle = right side.
def reset_robot():
    #reset base to right side 
    while not base_switch.pressed():
        base_motor.run(-100)
    #Set the position as angel zero
    base_motor.reset_angle(0)

# To reset gripper: We want to set open gripp as angel zero
def reset_gripper():
    robot_display('Reset gripper')
    reset_gripper = False
    while not reset_gripper:
        move_angel = 0
        #if center button is pressed
        if Button.CENTER in ev3.buttons.pressed():
            wait(500)
            #set open gripp as angel zero
            gripper_motor.reset_angle(0) 
            #go out from while loop
            reset_gripper = True
            continue
        elif Button.LEFT in ev3.buttons.pressed():
            #rotate base to the left
            wait(100)
            move_angel = 10
            gripper_motor.run_angle(MAX_SPEED,move_angel)
        elif Button.RIGHT in ev3.buttons.pressed():
            wait(100)
            #rotate base to the left
            move_angel = -10
            gripper_motor.run_angle(MAX_SPEED,move_angel)
        else: 
            wait(100)

# To define level for arm robot and return angle for each level
def set_arm():
    set_arm = False
    while not set_arm:
        move_angel = 0
        #if center button is pressed
        if Button.CENTER in ev3.buttons.pressed():
            wait(500)
            set_arm = True
            #return angle of arm
            return arm_motor.angle()
        elif Button.UP in ev3.buttons.pressed():
            wait(100)
            #move up the arm
            move_angel = 5
            arm_motor.run_angle(MAX_SPEED,move_angel)
        elif Button.DOWN in ev3.buttons.pressed():
            wait(100)
            #move down the arm
            move_angel = -5
            arm_motor.run_angle(MAX_SPEED,move_angel)
        else:
            wait(100)

# To set level of arm to move and set angel for each level
def set_level():
    #get into value for each level
    for level in ARM_LEVEL.keys():
    #get angle for each level
        robot_display('Set for: ' + level)
    #set angle for value for each level
        angle = set_arm()
        ARM_LEVEL[level] = angle
        wait(200)
        
# To move arm to given level
def move_arm(level):
    #get target level
    target_level = ARM_LEVEL.get(level)
    #get current level
    current_level = arm_motor.angle()
    #get diff level
    delta_level = target_level - current_level
    #rotate arm with diff level to target level
    arm_motor.run_angle(MAX_SPEED, delta_level) 

# To define position for base robot and return angle for each position
def set_base():
    set_base = False
    while not set_base:
        move_angel = 0
        #if center button is pressed
        if Button.CENTER in ev3.buttons.pressed():
            wait(500)
            set_base = True
            #return angle of base
            return base_motor.angle()
        elif Button.LEFT in ev3.buttons.pressed():
            wait(100)
            #rotate base to the left
            move_angel = 10
            base_motor.run_angle(MAX_SPEED,move_angel)
        elif Button.RIGHT in ev3.buttons.pressed():
            wait(100)
            #rotate base to the left
            move_angel = -10
            base_motor.run_angle(MAX_SPEED,move_angel)
        else: 
            wait(100)

# To get number to use in another function
def get_number(step=1):
    number = 0
    while True:
        robot_display(str(number))
        #if center button is pressed
        if Button.CENTER in ev3.buttons.pressed():
            wait(500)
            return number
        elif Button.UP in ev3.buttons.pressed():
            wait(100)
            #number plus one
            number += step
        elif Button.DOWN in ev3.buttons.pressed():
            wait(100)
            #number minus one
            number -= step
        wait(200)

# To set position and zone for base robot  
def set_positions():
    #set position amount
    robot_display('Total positions')
    wait(1500)
    positions = get_number()
    #define angle for all positions
    for number in range(positions):
        robot_display('Set position:'+ str(number+1))
        wait(1500)
        #get angle from buttons to dictionary
        POSITIONS[number+1] = set_base()
        wait(200)

    #set pick up position
    robot_display('Pick up' '\n' 'position:')
    wait(1500)
    pick_up_position = get_number()
    
    #set drop position
    robot_display('Drop position' '\n' 'for color:')
    wait(1500)
    drop_positions = {}
    for color in COLOR_LST:
        robot_display(color)
        wait(1500)
        number = get_number()
        drop_positions[color] = number
        wait(200)
    
    #return pick up and drop positions
    return (pick_up_position, drop_positions)

# To move base to given position        
def item_zone(position):
    target_position = POSITIONS.get(position)

    current_angle = base_motor.angle()
    delta_angle = target_position - current_angle

    base_motor.run_angle(MAX_SPEED, delta_angle)

# To detect the color of item and return item color as string
def detect_color():
    color = color_sensor.color()
    if color == Color.RED:
        color = "Red"
    elif color == Color.GREEN:
        color = "Green"
    elif color == Color.YELLOW:
        color = "Yellow"
    elif color == Color.BLUE:
        color = "Blue"
    else:
        color = 'Color not in list'
    return color

# To announce the color of item
def announce_color(color):
    ev3.speaker.say(color)

# To print the msg on display
def robot_display(msg):
    ev3.screen.clear()
    ev3.screen.print(msg)

# To pick item and control if gripper has item or not 
# If not robot gonna ask how long time need robot to wait before start pick item again 
def pick_item(position):
    picked = False
    item_zone(position)
    while not picked: 
        move_arm('down')
        close_gripper()
        # if gripper = 92 => no item
        current_angle = gripper_motor.angle()
        close_angle = 80
        if current_angle >= close_angle:
            # No item 
            open_gripper()
            move_arm('up') 
            #ask time for wait
            robot_display('Number for' '\n' 'wait time(ms)?')
            wait(1500)
            #input time by button
            wait_time = get_number(step=1000)
            #wait
            wait(wait_time)
            #pick again
        else: 
            # Have item
            move_arm('ColorSensor')
            picked = True

# To drop item at given zone
def drop_item(position):
    move_arm('up')
    item_zone(position)
    move_arm('down')
    open_gripper()
    move_arm('up')

def main():
    robot_display('Start set up')
    wait(1500)
    reset_gripper()
    set_level() 
    pick_up_position, drop_positions = set_positions()
    robot_display('Finish set up')
    while True:
        pick_item(pick_up_position)
        item_color = detect_color()
        ev3.speaker.say(item_color)
        
        #Get drop position if color in color list
        if item_color in drop_positions.keys():
            #get drop position from color list
            drop_position = drop_positions.get(item_color)
        elif item_color not in drop_positions.keys():
            #if not color in color list
            #ask number for position
            robot_display('Where do you want' '\n' 'to drop the item?')
            wait(1500)
            #get drop position from buttons
            drop_position = get_number()
            
        #drop item at the drop position
        drop_item(drop_position)

if __name__ == "__main__":
    main()

