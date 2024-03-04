import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ImageTransform
from .tasks import compress_image


logger = logging.getLogger(__name__)


@receiver(post_save, sender=ImageTransform)
def alerts_clear_cache_post_save(sender, instance, created, **kwargs):
    if created:
        compress_image_task = compress_image.delay(instance.pk)
        ImageTransform.objects.filter(
            pk=instance.pk
        ).update(compressor_task_id=compress_image_task.id)
