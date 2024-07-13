import subprocess
from clockWallpaper import ClockWallpaper
from time import sleep


if __name__ == "__main__":
    clockWallpaper = ClockWallpaper()

    while clockWallpaper.get_seconds() != "00":
        sleep(1)

    subprocess.run(["pythonw", "src/taskNoTime.pyw"])
