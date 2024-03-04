from django.contrib import admin

from .models import ImageTransform


class ImageTransformAdmin(admin.ModelAdmin):
    model = ImageTransform
    list_display = (
        "id", "raw_image", "processed_image", "is_compressed",
        "is_grey_scaled", "compressor_task_id", "created_at", "updated_at",
    )
    list_filter = (
        "is_compressed", "is_grey_scaled", "created_at", "updated_at",
    )
    readonly_fields = ("created_at", "updated_at", )

    class Meta:
        ordering = ('-created',)


admin.site.register(ImageTransform, ImageTransformAdmin)
