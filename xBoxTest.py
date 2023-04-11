# We use Pygame to access the Xbox One Controller
import pygame
from time import sleep
from pygame.constants import JOYBUTTONDOWN
pygame.init()

joysticks = []
for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()

# Print out the name of the controller
print(pygame.joystick.Joystick(0).get_name())

# Xbox Joystick Axis:
# Axis 0 up down, down value is -1, up value is 1
# Axis 1 Left, Right, Left value is: -1, right value is 1
# center is always 0

# Main Loop
while True or KeyboardInterrupt:

    # Check for joystick events
    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN: # Button Action
            if event.button == 0:
                print("button 0 down")
            if event.button == 1:
                print("button 1 down")
            if event.button == 2:
                print("button 2 down")
            if event.button == 3:
                print("button 3 down")
            if event.button == 4:
                print("button 4 down")
            if event.button == 5:
                print("button 5 down")
            if event.button == 6:
                print("button 6 down")
            if event.button == 7:
                print("button 7 down")
            if event.button == 8:
                print("button 8 down")
            if event.button == 9:
                print("button 9 down")
            if event.button == 10:
                print("button 10 down")
                
        if event.type == pygame.JOYAXISMOTION:
            axis = event.axis
            axisValue = event.value
            
            if axis < 2: # Left stick
                if axis == 0: # left/right
                    if axisValue < -0.5:
                        print(f"Left value: {axisValue:.2f} \n")
                        sleep(0.01)

                    if axisValue > 0.5:
                        print(f"Right value: {axisValue:.2f} \n")               
                        sleep(0.01)

                if axis == 1: # up/down
                    if axisValue < -0.5:
                        print(f"Up value: {axisValue:.2f} \n")
                        sleep(0.01)

                    if axisValue > 0.5:
                        print(f"Down value: {axisValue:.2f} \n")
                        sleep(0.01)

            
            if axis == 3: # Right stick 
                # if axis == 4: # left/right                              - Deadass, -cstick Left/Right just doesn't work
                #     if axisValue < -0.5:
                #         print(f"Left value: {axisValue:.2f} \n")
                #         sleep(0.01)

                #     if axisValue > 0.5:
                #         print(f"Right value: {axisValue:.2f} \n")               
                #         sleep(0.01)

                if axis == 3: # up/down                                 - Up/Down does though for -cstick
                    if axisValue < -0.5:
                        print(f"Up -cstick  : {axisValue:.2f} \n")
                        sleep(0.01)

                    if axisValue > 0.5:
                        print(f"Down -cstick  : {axisValue:.2f} \n")
                        sleep(0.01)
            
            if axis > 4:
                print("No, we're not using this.. dumbass")

                        
    """
    The Xbox 360 controller mapping has 6 axes, 11 buttons and 1 hat. The controller is recognized as "Xbox 360 Controller".

    Left Stick:

    Left -> Right   - Axis 0
    Up   -> Down    - Axis 1

    Right Stick:

    Left -> Right   - Axis 3
    Up   -> Down    - Axis 4

    Left Trigger:

    Out -> In       - Axis 2

    Right Trigger:

    Out -> In       - Axis 5

    Buttons:

    A Button        - Button 0
    B Button        - Button 1
    X Button        - Button 2
    Y Button        - Button 3
    Left Bumper     - Button 4
    Right Bumper    - Button 5
    Back Button     - Button 6
    Start Button    - Button 7
    L. Stick In     - Button 8
    R. Stick In     - Button 9
    Guide Button    - Button 10

    Hat/D-pad:

    Down -> Up      - Y Axis
    Left -> Right   - X Axis
    """