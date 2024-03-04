# Image-Processor


## Setup Instructions

### Step 1

Install Docker: https://docs.docker.com/engine/install/

### Step 2

Clone this repository and `cd` into the `Image-Processor` folder in a terminal

### Step 3

Start the containers
```
docker-compose up -d
```

## Admin Dashboard

You may enter the admin dashboard using the following information

**URL:** `http://localhost:8000/admin/`

**Username:** `admin`

**Password:** `admin`

## Requests

### cURL to upload an image
```
curl --location 'http://localhost:8000/image/transform/' \
--header 'Content-Type: application/json' \
--data '{
    "raw_image": "<image_base_64>"
}'
```

### cURL to retrieve images
```
curl --location --request GET 'http://localhost:8000/image/transform/' \
--header 'Content-Type: application/json'
```

You will notice that the upload image request will return to you a raw_image URL.

However, when you retrieve the images after some time (once they are processed), You will get a processed image URL. This image is compressed and converted to grey scale
