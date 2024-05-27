import ctypes
import os
import win32api, win32con
from PIL import Image, ImageDraw, ImageFont
import comtypes.client

# Generate the SHDocVw type library
comtypes.client.GetModule("shdocvw.dll")

# Import the generated SHDocVw module
import comtypes.gen.SHDocVw as SHDocVw

user = os.getlogin()


def saveWallpaper(imageName, ext, monitorId):
    winWallpaperPath = (
        r"C:\Users\\" + user + r"\AppData\Roaming\Microsoft\Windows\Themes"
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = os.path.join("..", "Images", imageName + ext)
    image = Image.open(os.path.join(current_dir, relative_path))
    image.save(os.path.join(winWallpaperPath, f"Transcoded_00{monitorId}" + ext))
    image.save(os.path.join(winWallpaperPath, f"TranscodedWallpaper" + ext))

    if os.path.exists(os.path.join(winWallpaperPath, f"Transcoded_00{monitorId}")):
        os.remove(os.path.join(winWallpaperPath, f"Transcoded_00{monitorId}"))
    if os.path.exists(os.path.join(winWallpaperPath, f"TranscodedWallpaper")):
        os.remove(os.path.join(winWallpaperPath, f"TranscodedWallpaper"))

    # # Renames the image to remove the extension
    os.rename(
        os.path.join(winWallpaperPath, "Transcoded_00" + monitorId + ext),
        os.path.join(winWallpaperPath, "Transcoded_00" + monitorId),
    )
    os.rename(
        os.path.join(winWallpaperPath, "TranscodedWallpaper" + ext),
        os.path.join(winWallpaperPath, "TranscodedWallpaper"),
    )


def updateWallpaper():
    # Replace "username" with the actual username
    wallpaper_path = (
        r"C:\Users\\"
        + user
        + r"\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper"
    )
    # Simulate a wallpaper change by sending a message
    # win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_DEACTIVATE, 0, 0)
    # win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_ACTIVATEAPP, 0, 0)
    win32api.PostMessage(
        win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, "Environment"
    )


def set_wallpaper_per_monitor():
    # Initialize COM
    comtypes.CoInitialize()

    CLSID_ActiveDesktop = comtypes.GUID("{75048700-EF1F-11D0-9888-006097DEACF9}")
    # Create an instance of IActiveDesktop
    iad = comtypes.client.CreateObject(CLSID_ActiveDesktop)

    # Define the paths to your wallpapers for each monitor
    wallpaper_paths = [
        # Replace with your actual image paths
        r"C:\Users\Alexis\Documents\GitHub\WallpaperSwitch\Images\MiniNez.png",
        r"C:\Users\Alexis\Documents\GitHub\WallpaperSwitch\Images\Aoi Ogata.jpg",
        r"C:\Users\Alexis\Documents\GitHub\WallpaperSwitch\Images\LucySexy.jpg",
    ]
    wallpaper_path = [
        # Replace with your actual image paths
        r"C:\Users\Alexis\Documents\GitHub\WallpaperSwitch\Images\MiniNez.png"
    ]

    # Get number of monitors (optional)
    monitors = iad.GetMonitorDesktopCount()

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


saveWallpaper("Aoi ogata", ".jpg", "1")
set_wallpaper_per_monitor()
