# install pywin32: pip install pywin32
import ctypes, win32con


def getWallpaper():
    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(
        win32con.SPI_GETDESKWALLPAPER, len(ubuf), ubuf, 0
    )
    return ubuf.value


print(getWallpaper())
# When having multiple screens, it's here : C:\Users\Alexis\AppData\Roaming\Microsoft\Windows\Themes
# Follow this : https://superuser.com/questions/1818823/how-to-convert-an-image-into-a-transcoded-image-for-use-as-a-wallpaper-on-wind
