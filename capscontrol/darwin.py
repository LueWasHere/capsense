# import rumps

# class AwesomeStatusBarApp(rumps.App):
#     def __init__(self):
#         super(AwesomeStatusBarApp, self).__init__("Awesome App")
#         self.menu = ["Preferences", "Silly button", "Say hi"]

#     @rumps.clicked("Preferences")
#     def prefs(self, _):
#         rumps.alert("jk! no preferences available!")

#     @rumps.clicked("Silly button")
#     def onoff(self, sender):
#         sender.state = not sender.state

#     @rumps.clicked("Say hi")
#     def sayhi(self, _):
#         rumps.notification("Awesome title", "amazing subtitle", "hi!!1") # possible darwin (macOS) solution should the below code not work...
import pystray
from PIL import Image
from time import sleep
from pynput.keyboard import Key, Controller
from keyboard import is_pressed
from sys import exit
import fcntl
# if my hunch is correct then the pystray library should work on Mac as well
# * NEEDS TO BE TESTED

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

def main_loop(icon):
    global running
    global timer
    global timer_sv

    icon.visible = True
    running = True
    keyboard = Controller()
    caps_lock = 0x04
    _KDGETLED = 0x4B31
    while running:
        # * Code should be the same as in linux
        bytes = struct.pack('I', 0)
        bytes = fcntl.ioctl(console_fd, _KDGETLED, bytes)
        [leds_state] = struct.unpack('I', bytes)
        status = leds_state & caps_lock != 0
        while status != 1:
            bytes = struct.pack('I', 0)
            bytes = fcntl.ioctl(console_fd, _KDGETLED, bytes)
            [leds_state] = struct.unpack('I', bytes)
            status = leds_state & caps_lock != 0
            sleep(
                1
            )
            if not running:
                exit(0)
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
            if capslock_state() == 1:
                print("Caps off")
                keyboard.press(Key.caps_lock)
                keyboard.release(Key.caps_lock)
            else:
                print("Caps isn't on...")
    exit(0)


def run():  # run the main programme, and set up the tray icon
    global timer
    global timer_sv
    image = Image.open("logo.png")

    def kill():  # if the user chooses to exit, kill the programme
        global running
        running = False
        print("Saving preferences and exiting...")
        with open("config.txt", "w") as config_file:
            config_file.write(str(timer_sv))
            config_file.close()
        icon.stop()
        print("Done.")

    def timer_10():
        global timer_sv
        print("Timer set to 10 seconds.")
        timer_sv = 10

    def timer_30():
        global timer_sv
        timer_sv = 30
        print("Timer set to 30 seconds.")

    def timer_60():
        global timer_sv
        timer_sv = 60
        print("Timer set to 1 minutes.")

    def timer_300():
        global timer_sv
        timer_sv = 60 * 5
        print("Timer set to 5 minutes.")

    # create the tray icon
    icon = pystray.Icon("Caps",
                        image,
                        "Capsense",
                        menu=(
                            pystray.MenuItem(
                                "Turn off Caps Lock after",
                                pystray.Menu(
                                    pystray.MenuItem("10 seconds", timer_10),
                                    pystray.MenuItem("30 seconds", timer_30),
                                    pystray.MenuItem("1 minute", timer_60),
                                    pystray.MenuItem("5 minutes", timer_300),
                                )),
                            pystray.MenuItem("Quit", kill),
                        ))

    icon.run(main_loop)
    exit(0)
