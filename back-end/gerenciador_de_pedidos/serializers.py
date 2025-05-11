from rest_framework import serializers
from django.utils import timezone
from rest_framework import serializers

from gerenciador_de_clientes.serializers import ClienteSerializer
from gerenciador_de_funcionarios.serializers import FuncionarioSerializer
from gerenciador_de_motoboys.serializers import MotoboySerializerResponse
from gerenciador_de_produtos.serializers import ProdutoSerializer
from .models import Pedido
from django.db.models import Sum


class PedidoSerializerResponse(serializers.ModelSerializer):
    produtos = ProdutoSerializer(many=True)
    cliente = ClienteSerializer()
    funcionario = FuncionarioSerializer()
    motoboy = MotoboySerializerResponse()
    data_hora_finalizacao = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(source='get_status_display')
    total_pedido = serializers.SerializerMethodField()  # Adiciona o campo total_pedido

    class Meta:
        model = Pedido
        fields = ['id', 'data_hora_inicio', 'data_hora_finalizacao', 'produtos', 'cliente', 'funcionario', 'motoboy', 'status', 'total_pedido']


    def validate(self, data):
        # Validação personalizada para garantir: cliente é obrigatório, pelo menos 1 produto no pedido
        if not data.get('cliente'):
            raise serializers.ValidationError({
                'cliente': 'O cliente é obrigatório para o pedido.'
            })
        
        if 'produtos' not in data or not data['produtos']:
            raise serializers.ValidationError({
                'produtos': 'O pedido deve conter pelo menos um produto.'
            })
            
        return data

    def validate_funcionario(self, value):
        if value is None:
            raise serializers.ValidationError("O campo 'funcionario' é obrigatório.")
        return value

    def get_produtos(self, obj):
        produtos_queryset = obj.produtos.all()
        produtos_serializer = ProdutoSerializer(produtos_queryset, many=True)
        return produtos_serializer.data

    def get_total_pedido(self, obj):  # Método para calcular o total do pedido
        total = obj.produtos.aggregate(Sum('preco'))['preco__sum']
        return total if total is not None else 0

class PedidoSerializerRequest(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['produtos', 'cliente', 'funcionario']
        extra_kwargs = {
            'cliente': {'required': True, 'allow_null': False},
            'funcionario': {'required': True},
            'produtos': {'required': True}
        }
    
    def validate(self, data):
        if data.get('cliente') is None:
            raise serializers.ValidationError({"cliente": "O cliente é obrigatório."})
        return data

    def validate_funcionario(self, value):
        if value is None:
            raise serializers.ValidationError("O campo 'funcionario' é obrigatório.")
        return value

    def create(self, validated_data):
        validated_data['data_hora_inicio'] = timezone.now()
        return super().create(validated_data)