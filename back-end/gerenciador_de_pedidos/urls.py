from django.urls import path
from .views import PedidoView, PedidoListView, PedidoDetailView, PedidoUpdateView, PedidoDeleteView, \
    PedidoAssignMotoboyView, PedidoActionView, PedidosAtribuidosMotoboysView, PedidosAtribuidosMotoboyView
from gerenciador_de_motoboys.views import PedidosMotoboyView

urlpatterns = [
    path('pedido', PedidoListView.as_view(), name='pedido-list'),
    path('pedido/add', PedidoView.as_view(), name='pedido-add'),
    path('pedido/<int:pk>', PedidoDetailView.as_view(), name='pedido-detail'),
    path('pedido/update/<int:pk>', PedidoUpdateView.as_view(), name='pedido-update'),
    path('pedido/delete/<int:pk>', PedidoDeleteView.as_view(), name='pedido-delete'),
    path('pedido/<int:pk>/atribuir-motoboy/<int:motoboy_id>', PedidoAssignMotoboyView.as_view(), name='pedido-atribuir-motoboy'),
    path('pedido/<int:pk>/action/<str:action>', PedidoActionView.as_view(), name='pedido-action'),
    path('pedido/motoboys', PedidosAtribuidosMotoboysView.as_view(), name='pedidos-atribuidos-motoboys'),
    path('pedido/motoboy/<int:motoboy_id>', PedidosMotoboyView.as_view(), name='pedidos-motoboy'),
]
