# @@@@@@ IMPORTS @@@@@@
from __future__ import print_function
import sys
import os
# sys.path.append("../")
import time
from DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board
import signal
import atexit
from pynput import keyboard
# IMPORTANT
# Requires the library "DFRobot_RaspberryPi_DC_Motor" to be in the current working directory
# That means in the same folder, or remove the commented sys.path for an adjustment


# @@@@@ VARIABLES @@@@@
board = Board(1, 0x10)    # Select bus 1, set address to 0x10



# @@@@@ FUNCTIONS @@@@@
def board_detect():
  l = board.detecte()
  print("Board list conform:")
  print(l)

def print_board_status():
  if board.last_operate_status == board.STA_OK:
    print("board status: everything ok")
  elif board.last_operate_status == board.STA_ERR:
    print("board status: unexpected error")
  elif board.last_operate_status == board.STA_ERR_DEVICE_NOT_DETECTED:
    print("board status: device not detected")
  elif board.last_operate_status == board.STA_ERR_PARAMETER:
    print("board status: parameter error, last operate no effective")
  elif board.last_operate_status == board.STA_ERR_SOFT_VERSION:
    print("board status: unsupport board framware version")

def board_detection():
  board_detect()
  while board.begin() != board.STA_OK:    # Board begin and check board status
    print_board_status()
    print("board begin faild")
    time.sleep(2)
  print("board begin success")

def handle_exit():
  board.motor_stop(board.ALL)   #stop all DC motor

# @@@Direction controls@@@
# Turns are not currently accurate. Must try different speed/time/without wires
# 2 is the weak motor
def go_straight():
  board.motor_movement([2], board.CW, 60)
  board.motor_movement([1], board.CW, 60)
  #time.sleep(0.5) deprecated from "Enter" days
def go_back():
  board.motor_movement([2], board.CCW, 60)
  board.motor_movement([1], board.CCW, 60)  
  #time.sleep(0.5) deprecated from "Enter" days
def swivel_left():  
  board.motor_movement([2], board.CW, 60)
  board.motor_movement([1], board.CCW, 60)
  #time.sleep(0.5) deprecated from "Enter" days
def swivel_right():
  board.motor_movement([1], board.CW, 60)
  board.motor_movement([2], board.CCW, 60)
  #time.sleep(0.5) deprecated from "Enter" days
def turn_left():  
  board.motor_movement([2], board.CW, 75)
  board.motor_movement([1], board.CW, 25)
  #time.sleep(0.5) deprecated from "Enter" days
def turn_right():
  board.motor_movement([1], board.CW, 75)
  board.motor_movement([2], board.CW, 25)
  #time.sleep(0.5) deprecated from "Enter" days
def keyPressed():
  holding 


# @@@@@ EXECUTION @@@@@@
if __name__ == "__main__":
  # Register signals - Behavior as the code exits
  atexit.register(handle_exit)
  signal.signal(signal.SIGTERM, handle_exit)
  board_detection() 
  
  board.set_encoder_disable(board.ALL)                  # Set selected DC motor encoder disable
  board.set_moter_pwm_frequency(1200)   # Set DC motor pwm frequency to 1000HZ

#while True:

keys_pressed = set()

def on_press(key, keys_pressed=keys_pressed):
    try:
        keys_pressed.add(key.char)

        if 'a' in keys_pressed and 'w' in keys_pressed:
            print('w and a pressed')
            turn_left()
        elif 'd' in keys_pressed and 'w' in keys_pressed:
            print('w and d pressed')
            turn_right()
        elif 'a' in keys_pressed:
            swivel_left()
            print('a pressed')
        elif 'w' in keys_pressed:
            print('w pressed')
            go_straight()
        elif 's' in keys_pressed:
            print('s pressed')
            go_back()
        elif 'd' in keys_pressed:
            print('d pressed')
            swivel_right()
        elif 'Num Lock' in keys_pressed:
            print('esc is pressed')
            board.motor_stop([1,2])
        elif 'p' in keys_pressed:
            print('P is pressed')
            board.motor_stop([1,2])


        '''
        elif 's' in keys_pressed and 'd' in keys_pressed:
            print('s and d pressed')
        elif 's' in keys_pressed and 'a' in keys_pressed:
            print('s and d pressed')
        '''
        
        #
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key, keys_pressed=keys_pressed):
    keys_pressed -= {key.char}
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
