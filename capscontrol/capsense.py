import pystray
from PIL import Image
from time import sleep
import keyboard
from sys import exit
from platform import system

class capsense:
    def __init__(self) -> None: # Bam, functionized.
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
            self.timer_sv = int(f.read().rstrip())
            f.close()
        self.timer = self.timer_sv
        self.running = True
        if system() != 'Windows':
            self.darwin_check = False # also applies for linux
        print("Done.")
    def capslock_state(self):
        import ctypes
        hll_dll = ctypes.WinDLL("User32.dll")
        vk_capital = 0x14
        return hll_dll.GetKeyState(vk_capital)
    # perfectly balanced... As all things should be...
    def main_loop(self, icon):
        def on_press(key): # Gone, reduced to a previous git commit...
            if key != "caps lock":
                self.timer = self.timer_sv
            else:
                if system() != 'Windows':
                    if self.darwin_check:
                        self.timer = self.timer_sv
                        self.darwin_check = False
                    else:
                        self.darwin_check = True
        keyboard.on_press(on_press)

        icon.visible = True
        while self.running:
            if system() == 'Windows':
                while not self.capslock_state():
                    # ponder the wonders of existence
                    sleep(1)
                    if self.timer != self.timer_sv:
                        self.timer = self.timer_sv
                    if not self.running:
                        exit(0)
            else:
                while not self.darwin_check:
                    # ponder the wonders of McIntosh
                    sleep(1)
                    if self.timer != self.timer_sv:
                        self.timer = self.timer_sv
                    if not self.running:
                        exit(0)

            if self.timer == 0:
                keyboard.press_and_release("caps lock")
                print("I did what I was designed to do!")

            print(f"{self.timer}...")
            sleep(1)
            self.timer -= 1
        icon.stop()
        
        

    def run(self):  # run the main PROGRAM, and set up the tray icon
        image = Image.open("logo.png")

        def kill():  # if the user chooses to exit, kill the PROGRAM
            self.running = False
            print("Saving preferences and exiting...")
            with open("config.txt", "w") as config_file:
                config_file.write(str(self.timer_sv))
                config_file.close()
            icon.stop()
            print("Done.")

        def timer_10():
            print("Timer set to 10 seconds.")
            self.timer_sv = 10

        def timer_30():
            self.timer_sv = 30
            print("Timer set to 30 seconds.")

        def timer_60():
            self.timer_sv = 60
            print("Timer set to 1 minutes.")

        def timer_300():
            self.timer_sv = 60 * 5
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
        icon.run(self.main_loop)
        exit(0)
