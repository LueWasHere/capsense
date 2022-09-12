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

# if my hunch is correct then the pystray library should work on Mac as well
# * NEEDS TO BE TESTED
from trayApp_handle import *  # Instead of copying and pasting code, let's just import the other file and use its function instead. hooray.

# I'd like to make this a function in the other file, instead of copy pasting. ;)
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

capslock_state()  # The capslock state cannot be determined with this function
# We should use a different method of grabbing the current caps lock status - one that works on Mac.
# TODO: find a way to grab the caps lock status on Mac.
run() # the run function handles getting the icon and running 'main_loop' function
