from rest_framework.serializers import ImageField
import base64
from django.core.files.base import ContentFile


class Base64ImageField(ImageField):
    """
    Поле для изображения в формате base64
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
