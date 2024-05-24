import ctypes
import os
import win32api, win32con
from PIL import Image, ImageDraw, ImageFont


def saveWallpaper(user, imageName, monitorId):
    winWallpaperPath = (
        r"C:\Users\\" + user + r"\AppData\Roaming\Microsoft\Windows\Themes"
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join("..", "Images", imageName + ".jpg")
    image = Image.open(os.path.join(current_dir, relative_path))
    image.save(os.path.join(winWallpaperPath, f"Transcoded_00{monitorId}.jpg"))

    if os.path.exists(os.path.join(winWallpaperPath, f"Transcoded_00{monitorId}")):
        os.remove(os.path.join(winWallpaperPath, f"Transcoded_00{monitorId}"))

    # Renames the image to remove the extension
    os.rename(
        os.path.join(winWallpaperPath, "Transcoded_00" + monitorId + ".jpg"),
        os.path.join(winWallpaperPath, "Transcoded_00" + monitorId),
    )


def changeWallpaper():
    # Get the absolute path of the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path from the current directory
    relative_path = os.path.join("..", "Images", "Aoi Ogata.jpg")

    # Get the absolute path using the constructed relative path
    absolute_path = os.path.normpath(os.path.join(current_dir, relative_path))

    # Set the desktop background using the absolute path
    ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, None, 0x0001 | 0x0002)


def updateWallpaper():
    # Replace "username" with the actual username
    wallpaper_path = r"C:\Users\username\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper"
    # Simulate a wallpaper change by sending a message
    win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_DEACTIVATE, 0, 0)
    win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_ACTIVATEAPP, 0, 0)


saveWallpaper("Alexis", "Aoi Ogata", "1")
changeWallpaper()
