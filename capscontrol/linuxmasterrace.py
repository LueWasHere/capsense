from time import sleep
import fcntl
import os
import struct
from keyboard import is_pressed

print("Fetching preferences...")
try:
    open("config.txt", "r")
except FileNotFoundError:
    print('"config.txt" not found!')
    with open("config.txt", "a") as f:
        f.write("10")
        f.close()
    print('"config.txt" made with default value of 10 seconds.')
with open("config.txt", "r") as f:
    timer_sv = int(f.read())
    f.close()
timer = timer_sv
running = False
print("Done.")

KDSETLED = 0x4B32
caps_lock = 0x04
_KDGETLED = 0x4B31

console_fd = os.open('/dev/tty', os.O_NOCTTY)
while True:
    bytes = struct.pack('I', 0)
    bytes = fcntl.ioctl(console_fd, _KDGETLED, bytes)
    [leds_state] = struct.unpack('I', bytes)
    # Turn on caps lock
    # fcntl.ioctl(console_fd, KDSETLED, 0x04)
    status = 0
    while True:
        status = leds_state & caps_lock != 0
        while status != 1:
            status = leds_state & caps_lock != 0
            sleep(
                1
            )  # just so we don't decrement the timer while caps-lock isn't on
        sleep(1)
        timer -= 1
        print(timer)

        # The biggest array you'll ever see - I am sure there is a better way to do this
        # TODO: Find a better way to do this
        # this is every button on the keyboard. like, every single one.
        buttons = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#',
            '$', '%', '^', '&', '*', '(', ')', '_', '+', '{', '}', '|', ':',
            '"', '<', '>', '?', '~', '`', '-', '=', '[', ']', '\\', ';', "'",
            ',', '.', '/', ' '
        ]
        # if any of the buttons are pressed, reset the timer
        for button in buttons:
            if is_pressed(button):
                timer = timer_sv
                print("Reset timer.")
        if timer == 0:  # if the timer is 0, turn off caps-lock
            timer = timer_sv
            if status == 1:
                print("Caps off")
                fcntl.ioctl(console_fd, KDSETLED, 0)
            else:
                print("Caps isn't on...")
