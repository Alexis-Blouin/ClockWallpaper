import configparser
import os
from configEditor import ConfigEditor

# https://docs.python.org/3.4/library/configparser.html#quick-start

if __name__ == "__main__":
    configEditor = ConfigEditor()
    USERNAME = os.getlogin()
    action = input(
        "What do you want to do? (1-add, 2-read user, 3-read default, 4-set_default): "
    )
    match action:
        case "1":
            config = configEditor.get_user_section(USERNAME)
            if config:
                print("A config already exists for this user")
                print(config["imagespath"])
            images_path = input("Images Path: ")
            if config:
                print(config["fontspath"])
            fonts_path = input("Fonts Path: ")
            if config:
                print(config["imagename"])
            image_name = input("Image Name: ")
            if config:
                print(config["monitorid"])
            monitor_id = input("Monitor Id: ")
            if config:
                configEditor.modify_user_section(
                    USERNAME, images_path, fonts_path, image_name, monitor_id
                )
            else:
                configEditor.add_user_section(
                    USERNAME, images_path, fonts_path, image_name, monitor_id
                )
        case "2":
            config = configEditor.get_user_section(USERNAME)
            if config:
                print(config)
            else:
                print("No config found for this user")
        case "3":
            print(configEditor.get_default_section())
        case "4":
            configEditor.set_default_section()
        case _:
            print("Invalid action")
