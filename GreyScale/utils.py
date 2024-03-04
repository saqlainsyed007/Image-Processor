import base64
import json
import os
import requests
import traceback

from io import BytesIO
from PIL import Image


def convert_to_greyscale(request_body):
    try:
        request_data = json.loads(request_body)

        image_id = request_data["image_id"]
        image_name = request_data['name']
        base_64_image_data = request_data['base_64_image_data']

        base64_string = base_64_image_data.split('base64,')[1]
        image_bytes = base64.b64decode(base64_string)
        image_stream = BytesIO(image_bytes)
        image = Image.open(image_stream)

        grey_scale_image = image.convert('L')
        grey_scale_image.save(os.path.join(os.environ['GREY_SCALE_IMAGE_DIR'], image_name))

        mark_grey_scaled(image_id)
    except Exception as xcptn:
        traceback.print_exc()
        print(f"Failed to process data {request_body}. Error {xcptn}")
        return


# Typically this will also happen via messaging
def mark_grey_scaled(image_id):
    backend_url = os.environ['BACKEND_URL']
    try:
        requests.patch(f"{backend_url}/image/transform/{image_id}/mark_grey_scaled/")
    except Exception as xcptn:
        print("Failed to update grey scaled status")
