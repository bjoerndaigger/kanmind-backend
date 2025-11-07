from django.urls import path

from .views import BoardListCreateView, BoardDetailView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='boards'), # GET / POST
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='boards-detail') # GET / PATCH / DELETE
]