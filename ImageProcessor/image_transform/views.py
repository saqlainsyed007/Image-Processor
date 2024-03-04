import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import ImageTransform
from .serializers import ImageTransformSerializer


logger = logging.getLogger()


# TODO: Add appropriate authentication
class ImageTransformViewSet(ModelViewSet):

    model = ImageTransform
    serializer_class = ImageTransformSerializer

    def get_queryset(self):
        return ImageTransform.objects.all()

    @action(detail=True, methods=["patch"])
    def mark_grey_scaled(self, request, pk):
        image_transform = self.get_object()
        image_transform.is_grey_scaled = True
        image_transform.save()
        return Response(status=status.HTTP_200_OK)
