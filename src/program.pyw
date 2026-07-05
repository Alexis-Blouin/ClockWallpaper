from clock_wallpaper import ClockWallpaper
from config_editor import ConfigEditor
from idesktop_wallpaper import IDesktopWallpaper
from utils import parse_text


if __name__ == "__main__":
    clockWallpaper = ClockWallpaper()

    configEditor = ConfigEditor()
    config_name = configEditor.get_config_name()
    # If no active config, we can stop the program there
    if config_name:
        config = configEditor.get_section(config_name)

        image_path = config["imagepath"]
        font_path = config["fontpath"]
        monitor = config["monitor"].split(",")
        hours_format = config["hours_format"]
        hours_params = parse_text(config["hours"])
        minutes_params = parse_text(config["minutes"])
        split_params = parse_text(config["split"])
        custom_params = parse_text(config["custom"])
        custom_char = config["custom_char"]

        img = clockWallpaper.draw_clock(
            image_path,
            (monitor[1], monitor[2]),
            font_path,
            hours_format,
            hours_params,
            minutes_params,
            split_params,
            custom_params,
            custom_char,
        )

        image_path = clockWallpaper.get_save_path(image_path)
        clockWallpaper.save_image(img, image_path)

        desktop_wallpaper = IDesktopWallpaper.CoCreateInstance()
        monitor = desktop_wallpaper.GetMonitorDevicePathAt(int(monitor[0]))
        desktop_wallpaper.SetWallpaper(monitor, image_path)
