import os
from clockWallpaper import ClockWallpaper
from configEditor import ConfigEditor
from iDesktopWallpaper import IDesktopWallpaper
from time import sleep


if __name__ == "__main__":
    clockWallpaper = ClockWallpaper()

    # while clockWallpaper.get_seconds() != "00":
    #     sleep(1)

    configEditor = ConfigEditor()
    username = os.getlogin()
    config = configEditor.get_user_section(username)
    if not config:
        config = configEditor.get_default_section()

    full_image_name = config["fullimagename"]
    images_path = config["imagespath"]
    monitor_id = int(config["monitorid"])
    full_font_name = config["fullfontname"]
    
    image_parts = full_image_name.split(".")
    image_name = image_parts[0]
    image_ext = image_parts[1]
    wallpaper = images_path + "\\" + image_name + "_out." + image_ext
    
    font_parts = full_font_name.split(".")
    font_name = font_parts[0]
    font_ext = font_parts[1]

    clockWallpaper.addClock(image_name, image_ext, font_name, font_ext)

    desktop_wallpaper = IDesktopWallpaper.CoCreateInstance()
    monitor_id = desktop_wallpaper.GetMonitorDevicePathAt(monitor_id)
    desktop_wallpaper.SetWallpaper(monitor_id, wallpaper)


# TODO Make this all pretty
# TODO create user interface where he can change a couple things like the font, the color, the position of the clock
