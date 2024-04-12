<<<<<<< Updated upstream
print ( "Hej alla")
print ( "hello world")
=======
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
    1: -112,     # zero point
    2: 0,    # ungefär 90° från zero point
    3: 47,   # ungefär 45° från andra position (135° från zero point) - drop off zone för gröna objekt
    4: 90    # ungefär 45° från tredje position (180° från zero point)
}

COLOR_LST = [Color.RED, Color.GREEN, Color.YELLOW]

# Function to close the gripper
def close_gripper():
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=35)
    print('close')

# Function to open the gripper
def open_gripper():
    gripper_motor.run_target(150, -90)
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
def announce_color():
    detected_color = detect_color()
    if detected_color == Color.RED:
        ev3.speaker.say("Red")
    elif detected_color == Color.GREEN:
        ev3.speaker.say("Green")
    elif detected_color == Color.YELLOW:
        ev3.speaker.say("Yellow")
    elif detected_color == Color.BLUE:
        ev3.speaker.say("Blue")
    else:
        ev3.speaker.say("No object detected")

def rotate_arm_until_end():
    # Spara den initiala vinkeln
    initial_angle = elbow_motor.angle()
    print('nuvarande')
    
    # Övervaka förändringen i vinkeln
    while True:
        elbow_motor.run(100)
        current_angle = elbow_motor.angle()
        # Om förändringen i vinkeln är mycket liten, anta att motorn har nått slutet
        if abs(current_angle - initial_angle) < 1:
            # Stanna motorn
            elbow_motor.stop(Stop.BRAKE)
            # Återställ vinkeln till 0
            elbow_motor.reset_angle(0)
            

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
        #elbow_up(50)
    return item_color

def reset_robot():
    while not base_switch.pressed():
        base_motor.run(-60)
    base_motor.run_angle(60,112)
    base_motor.reset_angle(0) 
    #rotate_arm_until_end()   
        
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

def main():
    elbow_up(45)
    reset_robot()
    for _ in range(3):
        open_gripper()
        pick_item(1)
        item_color = detect_color()
        if item_color == Color.RED:
            drop_item(3)
        elif item_color == Color.GREEN:
            drop_item(3)
        elif item_color == Color.YELLOW:
            drop_item(4)
        else:
            drop_item(4)
        elbow_up(90)
        item_C = elevated_position(2)
        if item_C == Color.RED:
            drop_item(3)
        elif item_C == Color.GREEN:
            drop_item(3)
        elif item_C == Color.YELLOW:
            drop_item(4)
        else:
            drop_item(4)
        elbow_up(90)
if __name__ == "__main__":
    main()
>>>>>>> Stashed changes
