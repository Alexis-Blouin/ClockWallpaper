import ClockWallpaper as cw
import IDesktopWallpaper as idw
from time import sleep


if __name__ == "__main__":
    clockWallpaper = cw.ClockWallpaper()

    while clockWallpaper.get_seconds() != "00":
        sleep(1)

    clockWallpaper.addClock("YorMirror", ".jpg", "FiraMono-Regular")

    desktop_wallpaper = idw.IDesktopWallpaper.CoCreateInstance()
    monitor_id = desktop_wallpaper.GetMonitorDevicePathAt(1)
    wallpaper = "C:\\Users\\Alexis\\Documents\\GitHub\\ClockWallpaper\\Images\\YorMirror_out.jpg"
    desktop_wallpaper.SetWallpaper(monitor_id, wallpaper)


# TODO Make this all pretty
# TODO crate user interface where he can change a couple things like the font, the color, the position of the clock
