from django.db import models


class ImageTransform(models.Model):

    raw_image = models.ImageField(upload_to="raw_images/", null=False, blank=False)
    processed_image = models.ImageField(upload_to="processed_images/", null=True, blank=True)
    is_compressed = models.BooleanField(default=False)
    is_grey_scaled = models.BooleanField(default=False)
    compressor_task_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")
