from PIL import Image, ImageDraw, ImageFont


def get_text_size(text, font):
    image = Image.new("RGBA", (1, 1), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    return draw.textsize(text, font)


def draw_text(text):
    """Take a string as input, return an image of the string."""
    font = ImageFont.truetype("fonts/UbuntuMono/UbuntuMono-R.ttf", 24)
    text_size = [d + 40 for d in get_text_size(text, font)]
    image = Image.new("RGBA", text_size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), text, (0, 0, 0), font=font)
    return image
