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
# 2 is the weak motor
def go_straight():
  board.motor_movement([2], board.CW, 90)
  board.motor_movement([1], board.CW, 90)
  #time.sleep(0.5) deprecated from "Enter" days
def go_back():
  board.motor_movement([2], board.CCW, 90)
  board.motor_movement([1], board.CCW, 90)  
  #time.sleep(0.5) deprecated from "Enter" days
def swivel_left():  
  board.motor_movement([2], board.CW, 90)
  board.motor_movement([1], board.CCW, 90)
  #time.sleep(0.5) deprecated from "Enter" days
def swivel_right():
  board.motor_movement([1], board.CW, 90)
  board.motor_movement([2], board.CCW, 90)
  #time.sleep(0.5) deprecated from "Enter" days
def turn_left():  
  board.motor_movement([2], board.CW, 90)
  board.motor_movement([1], board.CW, 30)
  #time.sleep(0.5) deprecated from "Enter" days
def turn_right():
  board.motor_movement([1], board.CW, 90)
  board.motor_movement([2], board.CW, 30)
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
  while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'a':
      print("\na is pressed")
      swivel_left()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'd':
      print("\nd is pressed")
      swivel_right()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'q':
      print("\nq is pressed")
      turn_left()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'e':
      print("\ne is pressed")
      turn_right()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'w':
      print("\nw is pressed")
      go_straight()
    if event.event_type == keyboard.KEY_DOWN and event.name == 's':
      print("\ns is pressed")
      go_back()
    if event.event_type == keyboard.KEY_DOWN and event.name == 'p':
      print("\n pause")
      board.motor_movement([2], board.CW, 15)
      board.motor_movement([1], board.CW, 10)
    elif keyboard.is_pressed('esc'):
      print("esc is pressed\n")
      board.motor_stop(board.all)
      print_board_status()
