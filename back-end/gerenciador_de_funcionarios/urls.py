from django.urls import path
from .views import FuncionarioView, FuncionarioListView, FuncionarioDetailView, FuncionarioUpdateView, FuncionarioDeleteView, FuncionarioLoginView

urlpatterns = [
    path('funcionario', FuncionarioListView.as_view(), name='funcionario-list'),
    path('funcionario/add', FuncionarioView.as_view(), name='funcionario-add'),
    path('funcionario/<int:pk>', FuncionarioDetailView.as_view(), name='funcionario-detail'),
    path('funcionario/update/<int:pk>', FuncionarioUpdateView.as_view(), name='funcionario-update'),
    path('funcionario/delete/<int:pk>', FuncionarioDeleteView.as_view(), name='funcionario-delete'),
    path('login', FuncionarioLoginView.as_view(), name='login'),
]
