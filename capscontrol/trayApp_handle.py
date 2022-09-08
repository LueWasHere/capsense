from tkinter import Menu
import pystray
from PIL import Image
from time import sleep
from pynput.keyboard import Key, Controller

def CAPSLOCK_STATE():
    import ctypes
    hllDll = ctypes.WinDLL ("User32.dll")
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
            sleep(1) # just so we don't decrement the time while caps-lock isn't on
        sleep(1)
        timer -= 1
        if timer == 0:
            timer = timer_sv
            if CAPSLOCK_STATE() == 1:
                print("Caps off")
                keyboard.press(Key.caps_lock)
                keyboard.release(Key.caps_lock)
            else:
                print("Caps isn't on...")
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
        timer_sv = 60*5
        print("Timer set to 5 minutes.")
    icon = pystray.Icon("Caps", image, menu=(
        pystray.MenuItem("Delay Before caps turn off", pystray.Menu(
            pystray.MenuItem("10 seconds", tens),
            pystray.MenuItem("30 seconds", thrs),
            pystray.MenuItem("1 minute", onem),
            pystray.MenuItem("5 minutes", fivm),
        )),
        pystray.MenuItem("Quit", kill),
    ))

    icon.run(main_loop)
