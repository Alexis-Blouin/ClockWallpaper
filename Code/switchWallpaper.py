import ctypes
import os

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path from the current directory
relative_path = os.path.join("..", "Images", "Aoi Ogata.jpg")

# Get the absolute path using the constructed relative path
absolute_path = os.path.normpath(os.path.join(current_dir, relative_path))

# Set the desktop background using the absolute path
ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path, 0)
