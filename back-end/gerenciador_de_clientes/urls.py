from django.urls import path
from .views import ClienteListView, ClienteDetailView, ClienteView, ClienteUpdateView, ClienteDeleteView, BuscaCepView

urlpatterns = [
    path('cliente', ClienteListView.as_view()),
    path('cliente/add', ClienteView.as_view()),
    path('cliente/<int:pk>', ClienteDetailView.as_view()),
    path('cliente/update/<int:pk>', ClienteUpdateView.as_view()),
    path('cliente/delete/<int:pk>', ClienteDeleteView.as_view()),
    path('buscacep/<str:cep>/', BuscaCepView.as_view())
]
