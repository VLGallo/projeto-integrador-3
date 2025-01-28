from django.urls import path
from .views import FuncionarioView, FuncionarioListView, FuncionarioDetailView, FuncionarioUpdateView, FuncionarioDeleteView, FuncionarioLoginView

urlpatterns = [
    path('funcionario', FuncionarioListView.as_view()),
    path('funcionario/add', FuncionarioView.as_view()),
    path('funcionario/<int:pk>', FuncionarioDetailView.as_view()),
    path('funcionario/update/<int:pk>', FuncionarioUpdateView.as_view()),
    path('funcionario/delete/<int:pk>', FuncionarioDeleteView.as_view()),
    path('login', FuncionarioLoginView.as_view()),
]
