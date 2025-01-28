from django.urls import path
from .views import ProdutoView, ProdutoDetailView, ProdutoUpdateView, ProdutoDeleteView, ProdutoListView

urlpatterns = [
    path('produto', ProdutoListView.as_view()),
    path('produto/add',ProdutoView.as_view()),
    path('produto/<int:pk>', ProdutoDetailView.as_view()),
    path('produto/update/<int:pk>', ProdutoUpdateView.as_view()),
    path('produto/delete/<int:pk>', ProdutoDeleteView.as_view()),
]

