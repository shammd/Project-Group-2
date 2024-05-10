# Project-Group-2

## Introduction

This project is an example of controlling LEGO® MINDSTORMS® EV3 robots using MicroPython. It includes code for controlling a robot arm to pick up and sort items, as well as code for coordinating communication between two robots.

## Getting Started

To get started with this project, follow these steps:

1. **Set Up EV3 MicroPython**: Download and install the [LEGO® EV3 MicroPython v2.0](https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3) on your EV3 brick.
2. **Connect EV3 to Computer**: Connect your EV3 robot to your computer using a USB cable.
3. **Upload Code**: Upload the Python scripts provided in this repository to your EV3 brick using your preferred file transfer method (e.g., drag and drop, command-line tool).

## Building and Running

To run the project:
1. **Start EV3**: Power on your EV3 robot.
2. **Run Main Program**: Execute the `main.py` script on your EV3 brick.
3. **Follow On-screen Instructions**: Follow the on-screen instructions to set up the robot arm, define positions, and operate the robot.

## Additional Notes
- This project assumes a basic understanding of LEGO® MINDSTORMS® EV3 and programming concepts.
- Make sure to customize the code according to your robot's configuration and requirements.

## Dependencies
This project requires the following dependencies:

- [LEGO® EV3 MicroPython v2.0](https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3)
- Pybricks library for EV3 MicroPython
- Python for running the scripts on your computer (for uploading to EV3 and testing)


## Features

- [x] US01B: As a user, I want the robot to pick up items from a designated position.
- [x] US02B: As a user, I want the robot to drop items off at a designated position.
- [x] US04B: As a user, I want the robot to tell me the color of an item at a designated position.
- [x] US09: As a user, I want the robot to check the pickup location periodically to see if a new item has arrived.
- [ ] US10: As a user, I want the robots to sort items at a specific time.
- [x] US11: As a user, I want two robots (from two teams) to communicate and work together on item sorting without colliding with each other.
- [x] US12: As a user, I want to be able to manually set the locations and heights of one pick up zone and two drop off zones. (Implemented either by manually dragging the arm to a position or using buttons)
- [x] US13: As a user, I want to easily reprogram the pickup and drop off zone of the robot.
- [ ] US14: As a user, I want to easily change the schedule of the robot pick up task.
- [ ] US15: As a user, I want to have an emergency stop button that immediately terminates the operation of the robot safely.
- [ ] US16: As a user, I want the robot to be able to pick an item up and put it in the designated drop off location within 5 seconds.
- [ ] US17: As a user, I want the robot to pick up items from a rolling belt and put them in the designated positions based on color and shape.
- [ ] US18: As a user, I want to have a pause button that pauses the robot's operation when the button is pushed and then resumes the program from the same point when I push the button again.
- [ ] US19: As a user, I want a very nice dashboard to configure the robot program and start some tasks on demand.
