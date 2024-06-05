import qrcode
import cloudinary.uploader
from tempfile import NamedTemporaryFile
from .models import *
import os
import uuid


def generate_qr_code(data):
    key = str(uuid.uuid4())
    print(key)
    qr_data = "https://genqr-ten.vercel.app/visit/"+key
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,   
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to a temporary file
    temp_file = NamedTemporaryFile(delete=False)
    img.save(temp_file.name)

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
