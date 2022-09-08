from tkinter import Menu
import pystray
from PIL import Image

def run():
    
    image = Image.open("icon.jpg")

    icon = pystray.Icon("Caps", image, menu=(
        pystray.MenuItem("Delay Before caps turn off", pystray.Menu(
            pystray.MenuItem("10 seconds", icon.stop()),
            pystray.MenuItem("30 seconds", icon.stop()),
            pystray.MenuItem("1 minute", icon.stop()),
            pystray.MenuItem("5 minutes", icon.stop()),
        )),
        pystray.MenuItem("Quit", icon.stop()),
    ))

    icon.run()