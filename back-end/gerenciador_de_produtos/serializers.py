from rest_framework import serializers
from .models import Produto
from django.db import IntegrityError

class ProdutoSerializer(serializers.ModelSerializer):
    preco = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco']

