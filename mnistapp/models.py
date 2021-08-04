from django.db import models

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=13)
    image = models.ImageField(default='media/default_image.png')
