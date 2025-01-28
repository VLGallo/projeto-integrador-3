from django.urls import path
from .views import MotoboyView, MotoboyListView, MotoboyDetailView, MotoboyUpdateView, MotoboyDeleteView

urlpatterns = [
    path('motoboy', MotoboyListView.as_view()),
    path('motoboy/add', MotoboyView.as_view()),
    path('motoboy/<int:pk>', MotoboyDetailView.as_view()),
    path('motoboy/update/<int:pk>', MotoboyUpdateView.as_view()),
    path('motoboy/delete/<int:pk>', MotoboyDeleteView.as_view()),
]

