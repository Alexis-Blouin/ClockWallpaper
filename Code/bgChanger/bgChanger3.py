import os
import sys
import glob
import time
import random
from PIL import Image
import win32api, win32con, win32gui

# Python 3 Script

# Variables for directories (one for each monitor/resolution)
dir1 = []
dir2 = []

# Let's move into directory which contains the images
# > Make sure to change below to directory
# > where you have saved your background images.
os.chdir("C:\\Users\\username\\Desktop\\bgs\\")

# Get images from both directories
# Each directory is equivalent to monitor's resolution
# > Change directories to match your resolution / dir name
def getImages():
	global dir1
	global dir2
	os.chdir("1920x1080")
	dir1 = glob.glob('./*.jpg')

	os.chdir("..\\1920x1200")
	dir2 = glob.glob('./*.jpg')
	# Return to original directory
	os.chdir("..")

# Merge 2 images together
def mergeIMG(img1, img2):
	img1 = '1920x1080\\' + img1
	img2 = '1920x1200\\' + img2
	images = [Image.open(x) for x in [img1, img2]]
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
		new_im.paste(im, (x_offset,0))
		x_offset += im.size[0]

	new_im.save('final.jpg', quality=100, subsampling=0)

# Function to actually set the wallpaper as tiled image
# > We will set background as a single image (which is 2 images merged)
def setWallpaper(path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "1")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1+2)

# ================================================================ #

# Let's get all images from both directories
getImages()

# Main program loop to switch images
try:
	while True:
		# Randomly select a image from each directory
		img1 = dir1[(random.randrange(0,len(dir1)))]
		img2 = dir2[(random.randrange(0,len(dir2)))]
		
		# Print message showing each image's name
		print("\n> Changing images: \n\t*" + img1 + "\n\t*" + img2)

		# Merge both images into a single image
		mergeIMG(img1, img2)

		# Finally we'll set the wallpaper as tiled image
		path = r'C:\Users\4Felipe\Desktop\bgs\final.jpg'
		setWallpaper(path)

		# Sleep for any amount of time you want (default = 600/10mins)
		time.sleep(600)
except KeyboardInterrupt:
	print('\n> Finished.')