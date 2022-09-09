from turtle import listen
import pystray
from PIL import Image
from time import sleep
from pynput.keyboard import Key, Controller
from keyboard import is_pressed
from sys import exit


def CAPSLOCK_STATE():
    import ctypes
    hllDll = ctypes.WinDLL("User32.dll")
    VK_CAPITAL = 0x14
    return hllDll.GetKeyState(VK_CAPITAL)


print("Fetching preferences...")
try:
    open("config.txt", "r")
except:
    print("\"config.txt\" not found!")
    with open("config.txt", "a") as f:
        f.write("10")
        f.close()
    print("\"config.txt\" made with default value of 10 seconds.")
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
    while running == True:
        while CAPSLOCK_STATE() != 1:
            sleep(
                1
            )  # just so we don't decrement the timer while caps-lock isn't on
            if running == False:
                exit(0)
        sleep(1)
        timer -= 1
        print(timer)

        # I take the walk of shame... I could find no other solution...
        if is_pressed('A'):
            timer = timer_sv
        elif is_pressed('B'):
            timer = timer_sv
        elif is_pressed('C'):
            timer = timer_sv
        elif is_pressed('D'):
            timer = timer_sv
        elif is_pressed('E'):
            timer = timer_sv
        elif is_pressed('F'):
            timer = timer_sv
        elif is_pressed('G'):
            timer = timer_sv
        elif is_pressed('H'):
            timer = timer_sv
        elif is_pressed('I'):
            timer = timer_sv
        elif is_pressed('J'):
            timer = timer_sv
        elif is_pressed('K'):
            timer = timer_sv
        elif is_pressed('L'):
            timer = timer_sv
        elif is_pressed('M'):
            timer = timer_sv
        elif is_pressed('N'):
            timer = timer_sv
        elif is_pressed('O'):
            timer = timer_sv
        elif is_pressed('P'):
            timer = timer_sv
        elif is_pressed('Q'):
            timer = timer_sv
        elif is_pressed('R'):
            timer = timer_sv
        elif is_pressed('S'):
            timer = timer_sv
        elif is_pressed('T'):
            timer = timer_sv
        elif is_pressed('U'):
            timer = timer_sv
        elif is_pressed('V'):
            timer = timer_sv
        elif is_pressed('W'):
            timer = timer_sv
        elif is_pressed('X'):
            timer = timer_sv
        elif is_pressed('Y'):
            timer = timer_sv
        elif is_pressed('Z'):
            timer = timer_sv
        if timer == 0:
            timer = timer_sv
            if CAPSLOCK_STATE() == 1:
                print("Caps off")
                keyboard.press(Key.caps_lock)
                keyboard.release(Key.caps_lock)
            else:
                print("Caps isn't on...")
    exit(0)


def run():
    global timer
    global timer_sv
    image = Image.open("icon.jpg")

    def kill():
        global running
        running = False
        print("quiting and saving preferences...")
        with open("config.txt", "w") as f:
            f.write(str(timer_sv))
            f.close()
        icon.stop()
        print("Done.")

    def tens():
        global timer_sv
        print("Timer set to 10 seconds.")
        timer_sv = 10

    def thrs():
        global timer_sv
        timer_sv = 30
        print("Timer set to 30 seconds.")

    def onem():
        global timer_sv
        timer_sv = 60
        print("Timer set to 1 minutes.")

    def fivm():
        global timer_sv
        timer_sv = 60 * 5
        print("Timer set to 5 minutes.")

    icon = pystray.Icon("Caps",
                        image,
                        menu=(
                            pystray.MenuItem(
                                "Delay Before caps turn off",
                                pystray.Menu(
                                    pystray.MenuItem("10 seconds", tens),
                                    pystray.MenuItem("30 seconds", thrs),
                                    pystray.MenuItem("1 minute", onem),
                                    pystray.MenuItem("5 minutes", fivm),
                                )),
                            pystray.MenuItem("Quit", kill),
                        ))

    icon.run(main_loop)
    exit(0)
