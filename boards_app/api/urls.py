from django.urls import path

from .views import BoardViewSet

urlpatterns = [
    path('boards/', BoardViewSet.as_view(), name='boards')
]