from qrcode_styled import QRCodeStyled
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import ImageColorMask

data = {
    "date": "2023.06.25",
    "title": "The Fast and the Furious: Tokyo Drift",
    "time": "14:00",
    "seats": [
        33,
        46
    ],
    "id": "clrbxrapbybyvvia",
    "urltoqr": "https://vincinemaApi.pythonanywhere.com/tikets/clrbxrapbybyvvia.png"
}

qr = QRCodeStyled()
qr_image = qr.get_image(str(data))

color_mask_image = Image.open('mask.jpg')  # Replace 'mask.png' with your custom color mask image

img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=ImageColorMask(
        color_mask_image=color_mask_image
    )
)

img.save('testqrr.png')
