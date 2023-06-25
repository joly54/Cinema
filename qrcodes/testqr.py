import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import ImageColorMask
from PIL import Image

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
qr.add_data(str(
{
      "id": "clrbxrapbybyvvia",
    }
))
qr.make()
mask = Image.open('mask.jpg')
#resize to 100x100 pixels
mask = mask.resize((100, 100))
img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=ImageColorMask(
        color_mask_image=mask
    )
)
img.save('TestQr.png')

