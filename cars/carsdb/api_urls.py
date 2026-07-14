from django.urls import include, path
from rest_framework.routers import DefaultRouter

from carsdb.api_views import PartViewSet

router = DefaultRouter()
router.register('parts', PartViewSet, basename='api-parts')

urlpatterns = [
    path('', include(router.urls)),
]
