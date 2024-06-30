import ctypes
import os
from time import sleep, strftime
import win32api, win32con
from PIL import Image, ImageDraw, ImageFont

user = os.getlogin()
global_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(global_path, "..", "Images")
font_path = os.path.join(global_path, "..", "Fonts")


def saveWallpaper(imageName, ext):
    winWallpaperPath = (
        r"C:\Users\\" + user + r"\AppData\Roaming\Microsoft\Windows\Themes"
    )

    current_dir = global_path
    relative_path = os.path.join("..", "Images", imageName + ext)
    image = Image.open(os.path.join(current_dir, relative_path))
    # image.save(os.path.join(winWallpaperPath, f"Transcoded_00{monitorId}" + ext))
    image.save(os.path.join(winWallpaperPath, f"TranscodedWallpaper" + ext))

    # if os.path.exists(os.path.join(winWallpaperPath, f"Transcoded_00{monitorId}")):
    #     os.remove(os.path.join(winWallpaperPath, f"Transcoded_00{monitorId}"))
    if os.path.exists(os.path.join(winWallpaperPath, f"TranscodedWallpaper")):
        os.remove(os.path.join(winWallpaperPath, f"TranscodedWallpaper"))

    # # Renames the image to remove the extension
    # os.rename(
    #     os.path.join(winWallpaperPath, "Transcoded_00" + monitorId + ext),
    #     os.path.join(winWallpaperPath, "Transcoded_00" + monitorId),
    # )
    os.rename(
        os.path.join(winWallpaperPath, "TranscodedWallpaper" + ext),
        os.path.join(winWallpaperPath, "TranscodedWallpaper"),
    )


def addClock(imageName, ext, font):
    path = os.path.join(image_path, imageName + ext)
    img = Image.open(path)
    # Get a drawing context
    draw = ImageDraw.Draw(img)

    # Load the fonts
    relative_path = os.path.join(font_path, f"{font}.ttf")
    font = ImageFont.truetype(relative_path, size=300)
    fontSplit = ImageFont.truetype(relative_path, size=150)

    x = 200
    y = 250
    positionHours = (x, y)
    positionMinutess = (x + 150, y + 150)
    positionSplit = (x + 450, y + 450)

    # Set the text and color
    split = "AM"
    hours = strftime("%H")
    if int(hours) > 12:
        hours = str(int(hours) - 12)
        split = "PM"
    if len(hours) == 1:
        hours = "0" + hours

    minutes = strftime("%M")
    minutes = str(int(minutes) + 1)
    if len(minutes) == 1:
        minutes = "0" + minutes
    colorHours = (180, 6, 20)
    colorMinutes = (232, 156, 54)

    # Draw the text on the image
    draw.text(positionHours, hours, fill=colorHours, font=font)
    draw.text(positionMinutess, minutes, fill=colorMinutes, font=font)
    draw.text(positionSplit, split, fill=colorHours, font=fontSplit)

    # Save the modified image as a new JPEG file
    output_path = os.path.join(image_path, f"{imageName}_out{ext}")
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


addClock("YorMirror", ".jpg", "FiraMono-Regular")
saveWallpaper("YorMirror_out", ".jpg")
updateWallpaper()

# TODO Make this all pretty
# TODO create a aloop for 60 seconds that check if the clock change then make the change

# TODO crate user interface where he can change a couple things like the font, the color, the position of the clock
