from django.urls import path
from .views import MotoboyView, MotoboyListView, MotoboyDetailView, MotoboyUpdateView, MotoboyDeleteView, MotoboyLoginView, PedidosMotoboyView

urlpatterns = [
    path('motoboy', MotoboyListView.as_view()),
    path('motoboy/add', MotoboyView.as_view()),
    path('motoboy/<int:pk>', MotoboyDetailView.as_view()),
    path('motoboy/update/<int:pk>', MotoboyUpdateView.as_view()),
    path('motoboy/delete/<int:pk>', MotoboyDeleteView.as_view()),
    path('motoboy/login', MotoboyLoginView.as_view()), # name='motoboy-login'),
    path('pedido/motoboy/<int:motoboy_id>', PedidosMotoboyView.as_view(), name='pedidos-motoboy'),
]

