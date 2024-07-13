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
    config = configEditor.get_default_section()

    image_path = config["imagepath"]
    font_path = config["fontpath"]
    monitor_id = int(config["monitorid"])
    hours_params = config["hours"].split(",")
    minutes_params = config["minutes"].split(",")
    split_params = config["split"].split(",")

    img = clockWallpaper.draw_clock(
        image_path,
        font_path,
        hours_params,
        minutes_params,
        split_params,
    )

    clockWallpaper.save_image(img, image_path)

    desktop_wallpaper = IDesktopWallpaper.CoCreateInstance()
    monitor = desktop_wallpaper.GetMonitorDevicePathAt(monitor_id)
    desktop_wallpaper.SetWallpaper(monitor, clockWallpaper.get_save_path(image_path))
