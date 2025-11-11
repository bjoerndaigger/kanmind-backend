from django.urls import path

from .views import RegistrationAPIView, CustomLoginView, email_check_view

urlpatterns = [
    path('registration', RegistrationAPIView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('email-check/', email_check_view)
]
