from clock_wallpaper import ClockWallpaper
from config_editor import ConfigEditor
from idesktop_wallpaper import IDesktopWallpaper
from time import sleep


if __name__ == "__main__":
    clockWallpaper = ClockWallpaper()

    configEditor = ConfigEditor()
    config_name = configEditor.get_config_name()
    config = configEditor.get_section(config_name)

    # TODO fix import by creating a util function 'parse_config' or whatever
    image_path = config["imagepath"]
    font_path = config["fontpath"]
    monitor = config["monitor"].split(",")
    hours_params = config["hours"].split(",")
    minutes_params = config["minutes"].split(",")
    split_params = config["split"].split(",")

    img = clockWallpaper.draw_clock(
        image_path,
        (monitor[1], monitor[2]),
        font_path,
        hours_params,
        minutes_params,
        split_params,
    )

    clockWallpaper.save_image(img, image_path)

    desktop_wallpaper = IDesktopWallpaper.CoCreateInstance()
    monitor = desktop_wallpaper.GetMonitorDevicePathAt(int(monitor[0]))
    desktop_wallpaper.SetWallpaper(monitor, clockWallpaper.get_save_path(image_path))
