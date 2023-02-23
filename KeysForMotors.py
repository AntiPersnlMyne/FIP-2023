# @@@@@@ IMPORTS @@@@@@
from __future__ import print_function
import sys
import os
# sys.path.append("../")
import time
from DFRobot_RaspberryPi_DC_Motor import DFRobot_DC_Motor_IIC as Board
import signal
import atexit
#new imports for key controls
import curses
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
  board.motor_movement([1, 2], board.CW, 100)
  time.sleep(2)
def go_back():
  board.motor_movement([1, 2], board.CCW, 100)
  time.sleep(2)
def turn_left():  
  board.motor_movement([1], board.CW, 100)
  board.motor_movement([2], board.CCW, 50)
  time.sleep(1)  
def turn_right():
  board.motor_movement([2], board.CW, 100)
  board.motor_movement([1], board.CCW, 50)
  time.sleep(1)
  
#More new key controls
actions = {
    curses.KEY_UP:  cameraDown,
    curses.KEY_DOWN:    cameraUp,
    curses.KEY_LEFT:    cameraFront,
    curses.KEY_RIGHT:   cameraFace,
}



# @@@@@ EXECUTION @@@@@@
if __name__ == "__main__":
  # Register signals - Behavior as the code exits
  atexit.register(handle_exit)
  signal.signal(signal.SIGTERM, handle_exit)
  board_detection() 
  
  
  board.set_encoder_disable(board.ALL)                  # Set selected DC motor encoder disable
  board.set_moter_pwm_frequency(100)   # Set DC motor pwm frequency to 1000HZ
  board.motor_movement([1, 2], board.CCW, 100)    # DC motor 1 movement, orientation clockwise
  #ccw on both moves backwards
  time.sleep(2)
  board.motor_movement([1, 2], board.CW, 100)
  #cw moves forward
  time.sleep(2)
  board.motor_movement([1], board.CW, 100)
  board.motor_movement([2], board.CCW, 100)
  #cw moves left
  time.sleep(2)
  board.motor_movement([2], board.CW, 100)
  board.motor_movement([1], board.CCW, 100)
  #cw moves right
  time.sleep(2)
  board.motor_stop(board.ALL)   #stop all DC motor
  print_board_status()

  def main(window):
    next_key = None
    while True:
        curses.halfdelay(1)
        if next_key is None:
            key = window.getch()
        else:
            key = next_key
            next_key = None
        if key != -1:
            # KEY PRESSED
            curses.halfdelay(3)
            action = actions.get(key)
            if action is not None:
                action()
            next_key = key
            while next_key == key:
                next_key = window.getch()
            # KEY RELEASED
            cameraFace()
