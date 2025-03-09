from django.urls import path
from .views import ClienteListView, ClienteDetailView, ClienteView, ClienteUpdateView, ClienteDeleteView, BuscaCepView

urlpatterns = [
    path('cliente', ClienteListView.as_view(), name="cliente_list"),
    path('cliente/add', ClienteView.as_view(), name="cliente_add"),
    path('cliente/<int:pk>', ClienteDetailView.as_view(), name="cliente_detail"),
    path('cliente/update/<int:pk>', ClienteUpdateView.as_view(), name="cliente_update"),
    path('cliente/delete/<int:pk>', ClienteDeleteView.as_view(), name="cliente_delete"),
    path('buscacep/<str:cep>/', BuscaCepView.as_view(), name="busca_cep")
]
