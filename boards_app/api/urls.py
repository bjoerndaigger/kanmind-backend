from django.urls import path
from rest_framework import routers

from .views import BoardViewSet

router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet)
urlpatterns = router.urls