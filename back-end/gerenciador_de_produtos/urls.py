from django.urls import path
from .views import ProdutoView, ProdutoDetailView, ProdutoUpdateView, ProdutoDeleteView, ProdutoListView

urlpatterns = [
    path('produto', ProdutoListView.as_view(), name= 'produto-list'),
    path('produto/add',ProdutoView.as_view(), name='produto-add'),
    path('produto/<int:pk>', ProdutoDetailView.as_view(), name='produto-detail'),
    path('produto/update/<int:pk>', ProdutoUpdateView.as_view(), name='produto-update'),
    path('produto/delete/<int:pk>', ProdutoDeleteView.as_view(), name='produto-delete'),
]

