import configparser
import os
from configEditor import ConfigEditor

# https://docs.python.org/3.4/library/configparser.html#quick-start

if __name__ == "__main__":
    configEditor = ConfigEditor()
    USERNAME = os.getlogin()
    action = input(
        "What do you want to do? (1-add, 2-read a config, 3-read default, 4-reset to default, 5-set a congif): "
    )
    match action:
        case "1":
            config_name = input("Config Name: ")
            config = configEditor.get_section(config_name)
            if config:
                print("This config already exists")
                print(config["imagespath"])
            images_path = input("Images Path: ")
            if config:
                print(config["fontspath"])
            fonts_path = input("Fonts Path: ")
            if config:
                print(config["imagename"])
            image_name = input("Image Name: ")
            if config:
                print(config["fontname"])
            font_name = input("Font Name: ")
            if config:
                print(config["monitorid"])
            monitor_id = input("Monitor Id: ")
            if config:
                configEditor.modify_section(
                    config_name,
                    images_path,
                    fonts_path,
                    image_name,
                    font_name,
                    monitor_id,
                    "200,250,300,180,6,20",
                    "400,450,300,232,156,54",
                    "650,700,150,180,6,20",
                )
            else:
                configEditor.add_section(
                    config_name,
                    images_path,
                    fonts_path,
                    image_name,
                    font_name,
                    monitor_id,
                    "200,250,300,180,6,20",
                    "400,450,300,232,156,54",
                    "650,700,150,180,6,20",
                )
        case "2":
            config_name = input("Config Name: ")
            config = configEditor.get_section(config_name)
            if config:
                print(config)
            else:
                print("This config doesn't exist")
        case "3":
            print(configEditor.get_default_section())
        case "4":
            configEditor.set_default_section()
        case "5":
            configEditor.set_config()
        case _:
            print("Invalid action")
