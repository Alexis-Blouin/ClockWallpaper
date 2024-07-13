import os
from time import strftime
from PIL import Image, ImageDraw, ImageFont


class ClockWallpaper:
    def draw_clock(
        self, image_path, font_path, hours_params, minutes_params, split_params
    ):
        draw, img = self.__open_image(image_path)

        hours, minutes, day_split = self.get_time()
        self.__draw_clock(draw, hours, font_path, hours_params)
        self.__draw_clock(draw, minutes, font_path, minutes_params)
        self.__draw_clock(draw, day_split, font_path, split_params)

        return img

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

    def __get_position(self, params):
        return (int(params[0]), int(params[1]))

    def __hex_to_rgb(self, params):
        return tuple(int(params[2][i : i + 2], 16) for i in (0, 2, 4)) + (255,)

    def __get_font(self, font_path, params):
        return ImageFont.truetype(font_path, size=int(params[3]))

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

    def __open_image(self, image_path):
        img = Image.open(image_path)
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
