import os

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import ImageColorMask
from PIL import Image, ImageFilter


def resize_mask(filename):
    img = Image.open("Ready_masks/" + filename)
    img = img.resize((300, 300))
    img.save("Ready_masks/" + filename)


file_list = os.listdir("../Posters/Ready_masks")
for file in file_list:
    print(file)
    resize_mask(file)
