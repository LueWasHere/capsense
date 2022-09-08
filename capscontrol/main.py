from sys import platform
if platform == "linux" or platform == "linux2":
    print("Linux master race")
    import subprocess
    subprocess.Popen(["python", "capscontrol/linuxmasterrace.py"], shell=False)
elif platform == "darwin":
    print("Cringe ass mac")
    exit(1)
elif platform == "win32" or platform == "win64":
    import trayApp_handle
    trayApp_handle.run()
