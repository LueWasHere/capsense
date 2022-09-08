from time import sleep
import trayApp_handle

class WINDOWS:
    def CAPSLOCK_STATE():
        import ctypes
        hllDll = ctypes.WinDLL ("User32.dll")
        VK_CAPITAL = 0x14
        return hllDll.GetKeyState(VK_CAPITAL)
    
    capsL = CAPSLOCK_STATE()

windows_con = WINDOWS()

print(windows_con.capsL)
sleep(1)
print(windows_con.capsL)