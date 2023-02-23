# @@@@@@ IMPORTS @@@@@@
from __future__ import print_function
import sys
import os
# sys.path.append("../")
import time
from DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board
import signal
import atexit
import keyboard
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
def go_straight():
  board.motor_movement([1, 2], board.CW, 50)
  time.sleep(0.5)
def go_back():
  board.motor_movement([1, 2], board.CCW, 50)
  time.sleep(0.5)
def turn_left():  
  board.motor_movement([1], board.CW, 60)
  board.motor_movement([2], board.CCW, 40)
  time.sleep(0.5)  
def turn_right():
  board.motor_movement([2], board.CW, 60)
  board.motor_movement([1], board.CCW, 40)
  time.sleep(0.5)

def rc_controls():
  key = input('press key')
  if key == 'a':
    print("a is pressed")
    turn_left()
  elif key == 's':
    print("s is pressed")
    go_back()
  elif key == 'w':
    print("w is pressed")
    go_straight()
  elif key == 'd':
    print("d is pressed")
    turn_right()
  elif key == 'q':
    print("q is pressed")
    board.motor_stop(board.all)
    print_board_status()
    

# @@@@@ EXECUTION @@@@@@
if __name__ == "__main__":
  # Register signals - Behavior as the code exits
  atexit.register(handle_exit)
  signal.signal(signal.SIGTERM, handle_exit)
  board_detection() 
  
  
  board.set_encoder_disable(board.ALL)                  # Set selected DC motor encoder disable
  board.set_moter_pwm_frequency(100)   # Set DC motor pwm frequency to 1000HZ
  while True:
    key = input('press key')
    if key == 'a':
      print("a is pressed")
      turn_left()
    elif key == 's':
      print("s is pressed")
      go_back()
    elif key == 'w':
      print("w is pressed")
      go_straight()
    elif key == 'd':
      print("d is pressed")
      turn_right()
    elif key == 'q':
      print("q is pressed")
      board.motor_stop(board.all)
      print_board_status()
