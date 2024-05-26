import ctypes
import os
import win32api, win32con
from PIL import Image, ImageDraw, ImageFont
import comtypes.client


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
    relative_path = os.path.join("..", "Images", "MiniNez.png")

    # Get the absolute path using the constructed relative path
    absolute_path = os.path.normpath(os.path.join(current_dir, relative_path))

    # Set the desktop background using the absolute path
    # ctypes.windll.user32.SystemParametersInfoW(0, 0, None, 0x0001 | 0x0002)

    SPI_SETDESKWALLPAPER = 0x0014
    SPIF_UPDATEINIFILE = 0x0001
    SPIF_SENDCHANGE = 0x0002

    # Refresh the current wallpaper
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        absolute_path,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
    )


def updateWallpaper():
    # Replace "username" with the actual username
    wallpaper_path = r"C:\Users\username\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper"
    # Simulate a wallpaper change by sending a message
    # win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_DEACTIVATE, 0, 0)
    # win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_ACTIVATEAPP, 0, 0)
    win32api.PostMessage(
        win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, "Environment"
    )


def set_wallpaper_per_monitor():
    # Initialize COM
    comtypes.CoInitialize()

    # Create an instance of IActiveDesktop
    iad = comtypes.client.CreateObject("ActiveDesktop")

    # Define the paths to your wallpapers for each monitor
    wallpaper_paths = [
        # Replace with your actual image paths
        r"C:\Users\Alexis\Documents\GitHub\WallpaperSwitch\MiniNez.png",
        r"C:\Users\Alexis\Documents\GitHub\WallpaperSwitch\Aoi Ogata.jpg",
        r"C:\Users\Alexis\Documents\GitHub\WallpaperSwitch\LucySexy.jpg",
    ]
    wallpaper_path = [
        # Replace with your actual image paths
        r"C:\Users\Alexis\Documents\GitHub\WallpaperSwitch\MiniNez.png"
    ]

    # Get number of monitors (optional)
    monitors = iad.GetMonitorDEsktopCount()

    # Set wallpaper for each monitor (using enumerate or explicit indices)
    # Choose the method that suits your needs
    # for i in range(min(monitors, len(wallpaper_paths))):
    #     iad.SetWallpaper(wallpaper_paths[i], i)

    for i in range(min(monitors, len(wallpaper_path))):
        iad.SetWallpaper(wallpaper_path[i], i)

    # Apply changes
    iad.ApplyChanges(0x0002)  # AD_APPLY_FORCE

    # Uninitialize COM
    comtypes.CoUninitialize()


# saveWallpaper("Alexis", "Aoi Ogata", "1")
# changeWallpaper()
set_wallpaper_per_monitor()
