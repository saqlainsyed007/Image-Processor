import base64
import io
import json
import logging

from celery import shared_task
from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from common.utils.rabbitmq import RabbitMQUtil
from .models import ImageTransform

logger = logging.getLogger(__name__)


@shared_task(max_retries=3)
def send_image_for_grey_scale(image_obj_id):
    logger.info(f"Send Grey Scale Request for Image {image_obj_id}")
    image_transform_obj = ImageTransform.objects.get(id=image_obj_id)
    if not image_transform_obj.is_compressed:
        print(f"Image in {image_transform_obj.id} is not compressed yet")
        return
    image_to_convert = image_transform_obj.processed_image
    pil_image = Image.open(image_transform_obj.processed_image.file)
    with open(image_to_convert.path, "rb") as image_file:
        image_base64 = (
            f"data:image/{pil_image.format.lower()};base64,"
            f"{base64.b64encode(image_file.read()).decode('utf-8')}"
        )
    request_data = {
        "image_id": image_transform_obj.id,
        "name": (
            f"{image_to_convert.name.split('.')[0].split('/')[-1]}"
            f".{pil_image.format}"
        ),
        "base_64_image_data": image_base64,
    }
    rabbitmq_util = RabbitMQUtil()
    rabbit_mq_exchange_name = settings.RABBIT_MQ_IMAGE_EXCHANGE_NAME
    rabbit_mq_topic_name = settings.RABBIT_MQ_GREY_SCALE_CONVERT_TOPIC_NAME
    rabbitmq_util.send_topic_message(
        exchange_name=rabbit_mq_exchange_name,
        topic_name=rabbit_mq_topic_name,
        message=json.dumps(request_data),
    )


@shared_task(max_retries=3)
def compress_image(image_obj_id):
    logger.info(f"Compress Image {image_obj_id}")
    compressed_image_quality = 80
    image_transform_obj = ImageTransform.objects.get(id=image_obj_id)
    compressed_image = Image.open(image_transform_obj.raw_image.path)
    # Create an empty buffer
    compressed_image_buffer = io.BytesIO()
    # Save the image with reduced quality to the buffer
    compressed_image.save(
        compressed_image_buffer,
        format=compressed_image.format,
        quality=compressed_image_quality,
    )
    compressed_image_buffer.seek(0)
    # Create a temp image file in memory
    processed_image_file = InMemoryUploadedFile(
        file=compressed_image_buffer,
        field_name=None,
        name=None,
        content_type=f'image/{compressed_image.format}',
        size=compressed_image_buffer.tell,
        charset=None
    )
    compressed_image_name = (
        f"{image_transform_obj.raw_image.name.split('.')[0].split('/')[-1]}"
        f"_compressed.{compressed_image.format}"
    )
    image_transform_obj.processed_image.save(
        name=compressed_image_name, content=processed_image_file,
    )
    image_transform_obj.is_compressed = True
    image_transform_obj.save()
    send_image_for_grey_scale(image_obj_id)


@shared_task
def simple_task(image_obj_id):
    print(image_obj_id)
