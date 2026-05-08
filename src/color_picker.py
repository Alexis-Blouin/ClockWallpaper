from colorthief import ColorThief

def get_dominant_colors(img_path, num_colors=5):
    color_thief = ColorThief(img_path)
    palette_rgb = color_thief.get_palette(num_colors)
    for color in palette_rgb:
        yield '#%02x%02x%02x' % color
