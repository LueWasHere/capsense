from platform import system
import sys  # instead of redifining sys.exit() as exit()
from time import sleep
import logging

import keyboard
import pystray
from PIL import Image

# setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
# debug logging
# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")


class capsense:
    def __init__(self) -> None:  # Bam, functionized.
        logging.info("Fetching preferences...")
        try:
            open("config.txt", "r", encoding="utf-8")
        except FileNotFoundError:
            # this should probably be 'info' instead of 'warning'. TODO think about this.
            logging.warning('"config.txt" not found!')
            with open("config.txt", "a", encoding="utf-8") as file:
                file.write("10")
                file.close()
            logging.info('"config.txt" made with default value of 10 seconds.')
        with open("config.txt", "r", encoding="utf-8") as file:
            self.timer_sv = int(file.read().rstrip())
            file.close()
        self.timer = self.timer_sv
        self.running = True
        if system() != "Windows":
            self.darwin_check = False  # also applies for linux
        logging.info("Done.")

    def capslock_state(self):
        import ctypes

        hll_dll = ctypes.WinDLL("User32.dll")
        vk_capital = 0x14
        return hll_dll.GetKeyState(vk_capital)

    def main_loop(self, icon):
        """Checks every so often to see if caps lock is on. If it is, it counts down
        Once the timer is up, it turns caps lock off."""

        def on_press(key):  # Gone, reduced to a previous git commit...
            if key != "caps lock":
                self.timer = self.timer_sv
            else:
                if system() != "Windows":
                    if self.darwin_check:
                        self.timer = self.timer_sv
                        self.darwin_check = False
                    else:
                        self.darwin_check = True

        keyboard.on_press(on_press)

        icon.visible = True
        while self.running:
            if system() == "Windows":
                while not self.capslock_state():
                    # ponder the wonders of existence
                    sleep(1)
                    if self.timer != self.timer_sv:
                        self.timer = self.timer_sv
                    if not self.running:
                        sys.exit(0)
            else:
                while not self.darwin_check:
                    # ponder the wonders of McIntosh
                    sleep(1)
                    if self.timer != self.timer_sv:
                        self.timer = self.timer_sv
                    if not self.running:
                        sys.exit(0)

            if self.timer == 0:
                keyboard.press_and_release("caps lock")
                logging.info("Turning off Caps Lock.")

            logging.debug(f"{self.timer} until disabling caps lock...")
            sleep(1)
            self.timer -= 1
        icon.stop()

    def run(self):
        """Creates the tray icon, runs the main loop, and saves preferences on exit."""
        image = Image.open("logo.png")

        def kill():  # if the user chooses to exit, kill the PROGRAM
            self.running = False
            print("Saving preferences and exiting...")
            with open("config.txt", "w", encoding="utf-8") as config_file:
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
        icon = pystray.Icon(
            "Caps",
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
                    ),
                ),
                pystray.MenuItem("Quit", kill),
            ),
        )
        icon.run(self.main_loop)
        sys.exit(0)
