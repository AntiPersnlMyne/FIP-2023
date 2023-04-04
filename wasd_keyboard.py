# from pynput import keyboard
# import time

# def pevent(e):
#     if e.event_type == keyboard.KEY_DOWN:
#         print("is down!")
#     elif e.event_type == keyboard.KEY_UP:
#         print("is up!")
#     else:
#         print("This should never happen!")
    
# def doW(event):
#     print("--W--")
#     pevent(event)
    
# def doA(event):
#     print("--A--")
#     pevent(event)
    
# keyboard.hook_key('w',doW)
# keyboard.hook_key('a',doA)

# keyboard.wait()

from pynput import keyboard

keys_pressed = set()

def on_press(key, keys_pressed=keys_pressed):
    try:
        keys_pressed.add(key.char)

        if 'a' in keys_pressed and 'w' in keys_pressed:
            print('w and a pressed')
        elif 'd' in keys_pressed and 'w' in keys_pressed:
            print('w and d pressed')
        elif 's' in keys_pressed and 'd' in keys_pressed:
            print('s and d pressed')
        elif 's' in keys_pressed and 'a' in keys_pressed:
            print('s and d pressed')
        elif 'a' in keys_pressed:
            #turn_left()
            print('a pressed')
        elif 'w' in keys_pressed:
            print('w pressed')
            #go_straight()
        elif 's' in keys_pressed:
            print('s pressed')
            #go_back()
        elif 'd' in keys_pressed:
            print('d pressed')
            #turn_right()
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


'''
Adding a speed boost key????
Voice synthesizer??
'''