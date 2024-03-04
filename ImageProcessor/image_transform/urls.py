from rest_framework.routers import DefaultRouter

from .views import ImageTransformViewSet

router = DefaultRouter()

router.register(r'', ImageTransformViewSet, basename='image_transformation_viewset')

urlpatterns = router.urls
