from rest_framework import serializers, viewsets
from .models import Image
import base64

class image_serializers(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Image
        fields = ('title', 'image')