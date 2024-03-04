from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import ImageTransform


class ImageTransformSerializer(serializers.ModelSerializer):

    raw_image = Base64ImageField(required=True)

    class Meta:
        model = ImageTransform
        fields = [
            "id", "raw_image", "processed_image", "is_compressed", "is_grey_scaled", "created_at", "updated_at"
        ]
        read_only_fields = [
            "id", "processed_image", "is_compressed", "is_grey_scaled", "created_at", "updated_at"
        ]

    def validate_raw_image(self, raw_image):
        if (
            not raw_image or
            (isinstance(raw_image, str) and not raw_image.strip())
        ):
            raise serializers.ValidationError("Please upload a valid image.")
        return raw_image
