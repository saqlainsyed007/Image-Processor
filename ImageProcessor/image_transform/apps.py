from django.apps import AppConfig


class ImageCompressorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image_transform'

    def ready(self):
        from . import signals
        return super().ready()
