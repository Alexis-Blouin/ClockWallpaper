import ctypes
import os
from time import sleep, strftime
import win32api, win32con
from PIL import Image, ImageDraw, ImageFont

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


def addClock(imageName, ext):
    path = f"Images/{imageName}{ext}"
    img = Image.open(path)
    # Get a drawing context
    draw = ImageDraw.Draw(img)

    # Set the font and position
    font = ImageFont.load_default(300)  # You can use a custom font as well
    width, height = img.size
    x = 200
    y = 350
    positionHours = (x, y)
    positionMinutess = (x + 200, y + 200)

    # Set the text and color
    hours = strftime("%H")
    minutes = strftime("%M")
    colorHours = (180, 16, 20)
    colorMinutes = (245, 174, 51)

    # Draw the text on the image
    draw.text(
        positionHours,
        hours,
        fill=colorHours,
        font=font,
    )
    draw.text(positionMinutess, minutes, fill=colorMinutes, font=font)

    # Save the modified image as a new JPEG file
    output_path = f"Images/{imageName}_out{ext}"
    img.save(output_path)


def updateWallpaper():
    # Replace "username" with the actual username
    wallpaper_path = (
        r"C:\Users\\"
        + user
        + r"\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper"
    )
    # Simulate a wallpaper change by sending a message
    # win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WA_INACTIVE, 0, 0)
    # win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_ACTIVATEAPP, 0, 0)

    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, None, 0)


addClock("YorMirror", ".jpg")
saveWallpaper("YorMirror_out", ".jpg", "1")
updateWallpaper()
