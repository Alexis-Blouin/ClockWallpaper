import os
from time import strftime
from PIL import Image, ImageDraw, ImageFont


class ClockWallpaper:
    def draw_clock(
        self,
        image_path,
        resolution,
        font_path,
        hours_params,
        minutes_params,
        split_params,
    ):
        draw, img = self.__open_image(image_path, resolution)

        hours, minutes, day_split = self.get_time()

        layers = (
            self.__get_layer(hours_params),
            self.__get_layer(minutes_params),
            self.__get_layer(split_params),
        )
        for i in range(3):
            if i == layers[0]:
                self.__draw_clock(draw, hours, font_path, hours_params)
            elif i == layers[1]:
                self.__draw_clock(draw, minutes, font_path, minutes_params)
            elif i == layers[2]:
                self.__draw_clock(draw, day_split, font_path, split_params)

        return img

    def __crop_to_ratio(self, img, ratio):
        # Get the dimensions of the image
        img_width, img_height = img.size
        target_width, target_height = ratio

        # Calculate aspect ratios
        img_aspect_ratio = img_width / img_height
        target_aspect_ratio = int(target_width) / int(target_height)

        # Determine how to crop based on the aspect ratios
        if img_aspect_ratio > target_aspect_ratio:
            # The image is wider than the target aspect ratio
            # Crop the width
            new_width = int(img_height * target_aspect_ratio)
            left = (img_width - new_width) / 2
            top = 0
            right = (img_width + new_width) / 2
            bottom = img_height
        else:
            # The image is taller than the target aspect ratio
            # Crop the height
            new_height = int(img_width / target_aspect_ratio)
            left = 0
            top = (img_height - new_height) / 2
            right = img_width
            bottom = (img_height + new_height) / 2

        # Crop the image
        cropped_img = img.crop((left, top, right, bottom))

        return cropped_img

    def get_time(self):
        day_split = strftime("%p")
        hours = strftime("%H")
        if int(hours) > 12:
            hours = str(int(hours) - 12)
        if len(hours) == 1:
            hours = "0" + hours
        minutes = strftime("%M")
        if len(minutes) == 1:
            minutes = "0" + minutes

        return hours, minutes, day_split

    def get_seconds(self):
        return strftime("%S")

    def __get_layer(self, params):
        return int(params[0])

    def __get_position(self, params):
        return (int(params[1]), int(params[2]))

    def __hex_to_rgb(self, params):
        hex_color = params[3]
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4)) + (255,)

    def __get_font(self, font_path, params):
        return ImageFont.truetype(font_path, size=int(params[4]))

    def __draw_clock(self, draw, text, font_path, params):
        position = self.__get_position(params)
        color = self.__hex_to_rgb(params)
        font = self.__get_font(font_path, params)
        draw.text(position, text, fill=color, font=font)

    def check_image(self, image_path):
        try:
            Image.open(image_path)
            return True
        except:
            return False

    def check_font(self, font_path):
        try:
            ImageFont.truetype(font_path)
            return True
        except:
            return False

    def __open_image(self, image_path, resolution):
        img = Image.open(image_path)
        img = self.__crop_to_ratio(img, resolution)
        return ImageDraw.Draw(img), img

    def save_image(self, img, image_path):
        img.save(self.get_save_path(image_path))

    def get_save_path(self, image_path):
        path_split = image_path.split("\\")
        folder_path = "\\".join(path_split[:-1])
        image_name = path_split[-1].split(".")[0]
        image_ext = path_split[-1].split(".")[1]
        output_path = os.path.join(folder_path, f"{image_name}_time.{image_ext}")
        return output_path
