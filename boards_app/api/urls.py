from django.urls import path

from .views import BoardListCreateView, BoardDetailView

urlpatterns = [
    path('', BoardListCreateView.as_view(), name='boards'), # GET / POST
    path('<int:pk>/', BoardDetailView.as_view(), name='boards_detail') # GET / PATCH / DELETE
]