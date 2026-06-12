from django.db import models

# Create your models here.

class registerModal(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.FileField(upload_to="avatars/",null=True, blank=True, max_length=255,default=None)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)