from django.db import models
from cloudinary.models import CloudinaryField
import uuid


class Qrcodes(models.Model):
    qr = CloudinaryField("qr", null=True, blank=True)
    logo = CloudinaryField("logo", null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    site = models.CharField(null=True, blank=True)
    file  = CloudinaryField("files", null=True, blank=True)
    file_name = models.CharField(null=True, blank=True)
    def __str__(self):
        return str(self.uuid)
