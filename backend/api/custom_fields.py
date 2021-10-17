import base64

import six
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class Base64ImageField(serializers.ImageField):
    """Custom ImageField to decode and save file from base64"""

    def to_internal_value(self, data):
        if isinstance(data, six.string_types) and data.startswith(
                'data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            try:
                data = ContentFile(
                    base64.b64decode(imgstr),
                    name=f'image.{ext}')
            except BaseException:
                raise ValidationError({'errors': 'Invalid image!'})
        return super(Base64ImageField, self).to_internal_value(data)
