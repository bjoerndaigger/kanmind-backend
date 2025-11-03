from django.urls import path

from .views import RegistrationAPIView, CustomLoginView

urlpatterns = [
    path('registration', RegistrationAPIView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login')
]
