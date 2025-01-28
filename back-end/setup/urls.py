from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("gerenciador_de_motoboys.urls")),
    path('', include("gerenciador_de_funcionarios.urls")),
    path('', include("gerenciador_de_clientes.urls")),
    path('', include("gerenciador_de_produtos.urls")),
    path('', include("gerenciador_de_pedidos.urls")),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
