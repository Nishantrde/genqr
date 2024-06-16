import qrcode
import cloudinary.uploader
from tempfile import NamedTemporaryFile
from .models import Qrcodes
import os
import uuid
from PIL import Image, ImageDraw
from django.core.files.uploadedfile import InMemoryUploadedFile

def generate_qr_code(data, url=None, logo=None, front=(0, 0, 0), crop="off", file=None, back=(255, 255, 255)):
    key = str(uuid.uuid4())
    print(f"Generated UUID: {key}")
    qr_data = "https://genqr-ten.vercel.app/"+url+"/" + key
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=front, back_color=back).convert("RGBA")

    overlay = Image.new("RGBA", img.size)
    draw = ImageDraw.Draw(overlay)

    center_x, center_y = img.width // 2, img.height // 2
    radius = min(img.width, img.height) // 2

    for r in range(radius, 0, -1):
        alpha = int(255 * (0.1 - r / radius))
        color = front + (alpha,)
        draw.ellipse(
            (center_x - r, center_y - r, center_x + r, center_y + r),
            fill=color,
            outline=None
        )
    img = Image.alpha_composite(img, overlay)

    if logo is not None:
        logo = Image.open(logo).convert("RGBA")
        logo_size = (img.width // 4, img.height // 4)
        logo = logo.resize(logo_size, Image.LANCZOS)
        
        if crop == "on":
            # Create a circular mask
            mask = Image.new("L", logo_size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0) + logo_size, fill=255)

            # Apply the mask to the logo
            logo.putalpha(mask)

        logo_position = (
            (img.width - logo_size[0]) // 2,
            (img.height - logo_size[1]) // 2
        )

        img.paste(logo, logo_position, logo)

    temp_file = NamedTemporaryFile(delete=False)
    img.save(temp_file.name, format='PNG')
    file_name = None
    cloudinary_fl_url = None
    if file is not None:
        try:
            if isinstance(file, InMemoryUploadedFile):
                # Handle InMemoryUploadedFile
                
                file_name = file.name
                file.seek(0)
                cloudinary_fl_response = cloudinary.uploader.upload(file, resource_type="auto")
            else:
                # Handle file path
                with open(file, 'rb') as fl:
                    file_name = fl.name
                    cloudinary_fl_response = cloudinary.uploader.upload(fl, resource_type="auto")
            cloudinary_fl_url = cloudinary_fl_response['url']
            print(f"Uploaded file URL: {cloudinary_fl_url}")
        except Exception as e:
            print(f"Error uploading file to Cloudinary: {e}")
            return None

    # Upload the QR code image to Cloudinary
    try:
        cloudinary_response = cloudinary.uploader.upload(temp_file.name, resource_type="image")
        cloudinary_url = cloudinary_response['url']
        print(f"Uploaded QR code URL: {cloudinary_url}")
    except Exception as e:
        print(f"Error uploading QR code to Cloudinary: {e}")
        return None
    finally:
        # Remove the temporary file
        temp_file.close()
        os.unlink(temp_file.name)

    # Save QR code data to the database
    obj = Qrcodes.objects.create(qr=cloudinary_url, uuid=key, site=data, file=cloudinary_fl_url, file_name=file_name)
    obj.save()

    return [cloudinary_url, qr_data, file_name]
