import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import ImageColorMask
from PIL import Image

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
qr.add_data(str(
{
      "username": "perepelukdanilo@gmail.com",
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
))
qr.make()
mask = Image.open('mask.jpg')
img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=ImageColorMask(
        color_mask_image=mask
    )
)
img.save('TestQr.png')
