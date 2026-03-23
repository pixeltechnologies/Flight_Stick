import time
import board
import analogio
import digitalio
import usb_hid

from adafruit_hid.gamepad import Gamepad

# Create gamepad
gp = Gamepad(usb_hid.devices)

# Hall sensors (analog)
x_axis = analogio.AnalogIn(board.GP26)
y_axis = analogio.AnalogIn(board.GP27)

# Buttons
btn1 = digitalio.DigitalInOut(board.GP14)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP

btn2 = digitalio.DigitalInOut(board.GP15)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.UP


def normalize(val):
    center = 32768
    deadzone = 2000

    if abs(val - center) < deadzone:
        return 0

    return int((val - center) / 256)  # scale to ~ -127 to 127


while True:
    x = normalize(x_axis.value)
    y = normalize(y_axis.value)

    # Send joystick axes
    gp.move_joysticks(x=x, y=y)

    # Buttons (1 and 2)
    if not btn1.value:
        gp.press_buttons(1)
    else:
        gp.release_buttons(1)

    if not btn2.value:
        gp.press_buttons(2)
    else:
        gp.release_buttons(2)

    time.sleep(0.01)
