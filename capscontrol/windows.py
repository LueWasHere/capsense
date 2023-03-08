import pystray
from PIL import Image
from time import sleep
import keyboard
from sys import exit


def capslock_state():
    import ctypes
    hll_dll = ctypes.WinDLL("User32.dll")
    vk_capital = 0x14
    return hll_dll.GetKeyState(vk_capital)

# I'd like to make this a function in the future, so we can just use fetch_prefs() in other files.
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
running = True
print("Done.")

# perfectly balanced... As all things should be...
def main_loop(icon):
    global running
    global timer
    global timer_sv
    
    def on_press(key): # Gone, reduced to a previous git commit...
        global timer
        global timer_sv
        if key != "caps lock":
            timer = timer_sv
    keyboard.on_press(on_press)

    icon.visible = True
    while running:
        while not capslock_state():
            # ponder the wonders of existence
            sleep(1)
            if timer != timer_sv:
                timer = timer_sv
            if not running:
                exit(0)

        if timer == 1:
            keyboard.press_and_release("caps lock")


        sleep(1)
        timer -= 1
        print(f"{timer}...")
    icon.stop()
    
    

def run():  # run the main programme, and set up the tray icon
    global timer
    global timer_sv
    global icon
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
