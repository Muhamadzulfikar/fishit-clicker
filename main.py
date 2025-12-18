from pynput.mouse import Button, Controller
from pynput import keyboard, mouse as mouse_module
import time
import threading

mouse = Controller()
isSpeedClick = False
isAutoPerfect = False
isPaused = False


def perfectMiddleMouse(x, y, button, pressed):
    if button == Button.middle and pressed:
        threading.Thread(target=lambda: (
            mouse.press(Button.left),
            time.sleep(0.3),
            mouse.release(Button.left)
        ), daemon=True).start()


def autoPerfect():
    global isAutoPerfect
    while isAutoPerfect:
        mouse.press(Button.left)
        time.sleep(0.3)
        mouse.release(Button.left)


def speedClick():
    global isSpeedClick
    while isSpeedClick:
        mouse.click(Button.left, 1)
        time.sleep(0.1)


def keyBinds(key):
    global isAutoPerfect, isSpeedClick, isPaused

    try:
        if key.char == 'f' and not isPaused:
            isAutoPerfect = not isAutoPerfect
            if isAutoPerfect:
                print("Auto Perfect ON")
                threading.Thread(target=autoPerfect, daemon=True).start()
            else:
                print("Auto Perfect OFF")

        elif key.char == 'j' and isPaused == False:
            isSpeedClick = not isSpeedClick
            if isSpeedClick:
                print("Speed Click ON")
                threading.Thread(target=speedClick, daemon=True).start()
            else:
                print("Speed Click OFF")
    except AttributeError:
        if key == keyboard.Key.esc:
            isPaused = not isPaused
            print("Paused" if isPaused else "Resumed")


with mouse_module.Listener(on_click=perfectMiddleMouse) as mouse_listener, \
     keyboard.Listener(on_press=keyBinds) as keyboard_listener:
    mouse_listener.join()
    keyboard_listener.join()
