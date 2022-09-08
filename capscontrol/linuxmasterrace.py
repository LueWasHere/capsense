from time import sleep

import fcntl
import os
import struct

KDSETLED = 0x4B32
caps_lock = 0x04
_KDGETLED = 0x4B31

console_fd = os.open('/dev/tty', os.O_NOCTTY)
while True:
    bytes = struct.pack('I', 0)
    bytes = fcntl.ioctl(console_fd, _KDGETLED, bytes)
    [leds_state] = struct.unpack('I', bytes)
    status = leds_state & caps_lock != 0
        # Turn on caps lock
        #fcntl.ioctl(console_fd, KDSETLED, 0x04)
    if status == 1:
        # Turn off caps lock
        fcntl.ioctl(console_fd, KDSETLED, 0)