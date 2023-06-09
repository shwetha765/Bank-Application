from django.db import models


# Create your models here.
class File(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to="files")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)