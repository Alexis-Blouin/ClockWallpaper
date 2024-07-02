import configparser
import os

USERNAME = os.getlogin()
# https://docs.python.org/3.4/library/configparser.html#quick-start

# Creates the file
# config = configparser.ConfigParser()
# config["DEFAULT"] = {
#     "ImagesPath": "C:\\Users\\Alexis\\Documents\\GitHub\\ClockWallpaper\\Images",
#     "FontsPath": "C:\\Users\\Alexis\\Documents\\GitHub\\ClockWallpaper\\Fonts",
# }
# with open("config/config.ini", "w") as configfile:
#     config.write(configfile)


# Modifies the file
# config = configparser.ConfigParser()
# config.read("config/config.ini")
# config.add_section(USERNAME)
# config[USERNAME] = {
#     "ImagesPath": "C:\\Users\\Alexis\\Documents\\GitHub\\ClockWallpaper\\Images",
#     "FontsPath": "C:\\Users\\Alexis\\Documents\\GitHub\\ClockWallpaper\\Fonts",
#     "ImageName": "YorMirror",
# }
# with open("config/config.ini", "w") as configfile:
#     config.write(configfile)

# Reads the file
config = configparser.ConfigParser()
config.read("config/config.ini")
print(config.defaults())
print(config[USERNAME]["ImageName"])
