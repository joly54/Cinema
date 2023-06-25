import os

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import ImageColorMask
from PIL import Image, ImageFilter


def image_gen(name):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data('https://vincinemaApi.pythonanywhere.com/tikets/clrbxrapbybyvvia.png')
    qr.make()
    mask = Image.open(name)
    # get average color
    if name != "13.jpg":
        mask = mask.filter(ImageFilter.GaussianBlur(20))
    else:
        mask = mask.filter(ImageFilter.GaussianBlur(1))


    if not os.path.exists('Ready_masks'):
        os.makedirs('Ready_masks')
    mask.save("Ready_masks/" + name[0:name.find(".")] + "_mask.png")


os.chdir('mask')
images = os.listdir()
print(images)
count = 1

for image in images:
    print(f'Image {count} of {len(images)}')
    count += 1
    image_gen(f'{image}')
