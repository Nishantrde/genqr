import qrcode
import cloudinary.uploader
from tempfile import NamedTemporaryFile
from .models import *
import os
import uuid
from PIL import Image, ImageDraw, ImageFilter


def generate_qr_code(data):
    key = str(uuid.uuid4())
    print(key)
    qr_data = "https://genqr-ten.vercel.app/visit/"+key
    qr = qrcode.QRCode(#qrcode
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=(0, 255, 0), back_color=(0, 0, 0)).convert("RGBA")

    overlay = Image.new("RGBA", img.size)
    draw = ImageDraw.Draw(overlay)

    center_x, center_y = img.width // 2, img.height // 2
    radius = min(img.width, img.height) // 2
    
    for r in range(radius,0,-1):
        alpha = int(255 * (0.2 - r/radius))
        color = (24, 21, 245, alpha)
        draw.ellipse(
            (center_x - r, center_y - r, center_x + r, center_y + r),
            fill =  color,
            outline = None
        )
    img = Image.alpha_composite(img, overlay)

    # Save QR code image to a temporary file
    temp_file = NamedTemporaryFile(delete=False)
    img.save(temp_file.name, format='PNG')

    # Upload image to Cloudinary
    cloudinary_response = cloudinary.uploader.upload(temp_file.name)
    cloudinary_url = cloudinary_response['url']

    # Remove temporary file
    temp_file.close()
    os.unlink(temp_file.name)

    # Save QR code data to the database
    obj = Qrcodes.objects.create(qr=cloudinary_url,uuid = key, site=data)
    obj.save()
    
    return cloudinary_url
