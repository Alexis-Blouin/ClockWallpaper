import os
from time import strftime
from PIL import Image, ImageDraw, ImageFont


class ClockWallpaper:
    def add_clock(self, config):
        images_path = config["imagepath"]
        full_image_name = config["fullimagename"]
        image_parts = full_image_name.split(".")
        image_name = image_parts[0]
        image_ext = image_parts[1]

        fonts_path = config["fontpath"]
        full_font_name = config["fullfontname"]
        font_parts = full_font_name.split(".")
        font_name = font_parts[0]
        font_ext = font_parts[1]

        draw, img = self.__open_image(images_path, image_name, image_ext)

        hours_params = config["hours"].split(",")
        minutes_params = config["minutes"].split(",")
        split_params = config["split"].split(",")

        positionHours, positionMinutes, positionSplit = self.__set_position(
            [hours_params, minutes_params, split_params]
        )

        hours_color = self.__hex_to_rgb(hours_params)
        minutes_color = self.__hex_to_rgb(minutes_params)
        split_color = self.__hex_to_rgb(split_params)

        hours_font = self.__set_font(fonts_path, font_name, font_ext, hours_params)
        minutes_font = self.__set_font(fonts_path, font_name, font_ext, minutes_params)
        split_font = self.__set_font(fonts_path, font_name, font_ext, split_params)

        hours, minutes, day_split = self.get_time()
        self.__draw_clock(draw, positionHours, hours, hours_color, hours_font)
        self.__draw_clock(draw, positionMinutes, minutes, minutes_color, minutes_font)
        self.__draw_clock(draw, positionSplit, day_split, split_color, split_font)

        self.__save_image(img, images_path, image_name, image_ext)

    def get_time(self):
        day_split = "AM"
        hours = strftime("%H")
        if int(hours) >= 12:
            day_split = "PM"
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

    def __open_image(self, images_path, image_name, image_ext):
        path = os.path.join(images_path, f"{image_name}.{image_ext}")
        img = Image.open(path)
        return ImageDraw.Draw(img), img

    def __save_image(self, img, images_path, image_name, image_ext):
        output_path = os.path.join(images_path, f"{image_name}_time.{image_ext}")
        img.save(output_path)

    def __set_position(self, params):
        result = []
        for param in params:
            result.append((int(param[0]), int(param[1])))
        return result[0], result[1], result[2]

    def __hex_to_rgb(self, params):
        return tuple(int(params[2][i : i + 2], 16) for i in (0, 2, 4)) + (255,)

    def __set_font(self, fonts_path, font_name, font_ext, params):
        font_path = os.path.join(fonts_path, f"{font_name}.{font_ext}")
        return ImageFont.truetype(font_path, size=int(params[3]))

    def __draw_clock(self, draw, position, text, color, font):
        draw.text(position, text, fill=color, font=font)
