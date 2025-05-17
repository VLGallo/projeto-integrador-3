from rest_framework import serializers
from .models import Produto
from django.db import IntegrityError
from django.core.validators import MinValueValidator
from decimal import Decimal

class ProdutoSerializer(serializers.ModelSerializer):
    preco = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], error_messages={
        'max_digits': 'O preço não pode ter mais que 10 dígitos no total.',
        'min_value':'O preço deve ser positivo.'
        }
    )
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco']

def validate_preco(self, value):
    #Validação personalizada para o preço
    # Verifica se é positivo
    if value <= Decimal('0'):
        raise serializers.ValidationError("Certifique-se que este valor seja maior ou igual a 0.01.")
            
    # Verifica o número máximo de dígitos
    str_value = str(value).replace('.', '')
    if len(str_value) > 10:
        raise serializers.ValidationError("O preço não pode ter mais que 10 dígitos no total.")
            
    return value