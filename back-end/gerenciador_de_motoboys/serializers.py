from rest_framework import serializers
from gerenciador_de_funcionarios.models import Funcionario
from gerenciador_de_funcionarios.serializers import FuncionarioSerializer
from .models import Motoboy
import re


class MotoboySerializerRequest(serializers.ModelSerializer):
    funcionario = serializers.IntegerField(write_only=True)

    class Meta:
        model = Motoboy
        fields = ['id', 'nome', 'telefone', 'placa', 'funcionario']

    # Função para tratar telefone
    def validate_telefone(self, value):
        telefone_limpo = re.sub(r'\D', '', value)

        if telefone_limpo.startswith('0'):
            telefone_limpo = telefone_limpo[1:]

        if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
            raise serializers.ValidationError("Telefone inválido. Deve conter 10 ou 11 dígitos.")

        return telefone_limpo


    # Função para remover traços e espaços da placa
    def validate_placa(self, value):
        # Remove traços, espaços e transforma tudo em maiúsculas
        placa_limpa = re.sub(r'[^A-Za-z0-9]', '', value).upper()
        if len(placa_limpa) != 7:
            raise serializers.ValidationError("Placa inválida. Deve conter 7 caracteres.")
        return placa_limpa


    def create(self, validated_data):
        funcionario = validated_data.pop('funcionario')
        funcionario = Funcionario.objects.get(pk=funcionario)
        validated_data['funcionario'] = funcionario
        return super().create(validated_data)


    def update(self, instance, validated_data):
        # Não permitir a atualização do cadastrante
        validated_data.pop('funcionario', None)
        return super().update(instance, validated_data)


class MotoboySerializerResponse(serializers.ModelSerializer):
    funcionario = FuncionarioSerializer()

    class Meta:
        model = Motoboy
        fields = ['id', 'nome', 'telefone', 'placa', 'funcionario']


class MotoboySerializerResponse(serializers.ModelSerializer):
    funcionario = FuncionarioSerializer()

    class Meta:
        model = Motoboy
        fields = ['id', 'nome', 'telefone', 'placa', 'funcionario']
