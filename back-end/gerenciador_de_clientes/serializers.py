from rest_framework import serializers
from .models import Cliente
import re

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'telefone', 'cep', 'logradouro', 'numero', 'complemento', 'bairro']

    def validate_telefone(self, value):
        # Limpar telefone (remover espaços, parênteses e traços)
        telefone_limpo = re.sub(r'\D', '', value)  # Remove tudo que não é número

        # Remove o zero na frente do DDD, se existir
        if telefone_limpo.startswith('0'):
            telefone_limpo = telefone_limpo[1:]

        if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
            raise serializers.ValidationError("Telefone inválido. Deve conter 10 ou 11 dígitos.")

        return telefone_limpo
