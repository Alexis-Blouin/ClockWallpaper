import ctypes
import os
from time import sleep, strftime
import win32api, win32con
from PIL import Image, ImageDraw, ImageFont

user = os.getlogin()
global_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(global_path, "..", "Images")
font_path = os.path.join(global_path, "..", "Fonts")


class ClockWallpaper:

    def addClock(self, imageName, ext, font):
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
        hours, minutes, day_split = self.get_time()
        colorHours = (180, 6, 20)
        colorMinutes = (232, 156, 54)

        # Draw the text on the image
        draw.text(positionHours, hours, fill=colorHours, font=font)
        draw.text(positionMinutess, minutes, fill=colorMinutes, font=font)
        draw.text(positionSplit, day_split, fill=colorHours, font=fontSplit)

        # Save the modified image as a new JPEG file
        output_path = os.path.join(image_path, f"{imageName}_out{ext}")
        img.save(output_path)

    def get_time(self):
        day_split = "AM"
        hours = strftime("%H")
        if int(hours) >= 12:
            day_split = "PM"
            if int(hours) > 12:
                hours = str(int(hours) - 12)
        if len(hours) == 1:
            hours = "0" + hours
        minutes = strftime("%M")
        if len(minutes) == 1:
            minutes = "0" + minutes

        return hours, minutes, day_split

    def get_seconds(self):
        return strftime("%S")
