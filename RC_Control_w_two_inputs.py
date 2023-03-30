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
def right_forward():
  board.motor_movement([2], board.CW, 50)
  
def right_neutral():
  board.motor_movement([2], board.CW, 10)
  
def right_back():  
  board.motor_movement([2], board.CCW, 50)
  
  
def left_forward():
  board.motor_movement([1], board.CW, 50)
  
def left_neutral():
  board.motor_movement([1], board.CW, 10)
  
def left_back():
  board.motor_movement([1], board.CCW, 50)
  

  

# @@@@@ EXECUTION @@@@@@
if __name__ == "__main__":
  # Register signals - Behavior as the code exits
  atexit.register(handle_exit)
  signal.signal(signal.SIGTERM, handle_exit)
  board_detection() 
  
  
  board.set_encoder_disable(board.ALL)                  # Set selected DC motor encoder disable
  board.set_moter_pwm_frequency(1200)   # Set DC motor pwm frequency to 1000HZ
  while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
      left_forward()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'a':
      left_neutral()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'z':
      left_back()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'w':
      right_forward()
    if event.event_type == keyboard.KEY_DOWN and event.name == 's':
      right_neutral()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'x':
      right_back()
    
    elif keyboard.is_pressed('esc'):
      print("esc is pressed")
      board.motor_stop(board.all)
      print_board_status()
