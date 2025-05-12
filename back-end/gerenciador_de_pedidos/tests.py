from django.test import TestCase
from django.utils import timezone
from datetime import datetime, timedelta
from gerenciador_de_pedidos.models import Pedido
from gerenciador_de_clientes.models import Cliente
from gerenciador_de_funcionarios.models import Funcionario
from gerenciador_de_produtos.models import Produto
from gerenciador_de_motoboys.models import Motoboy
from rest_framework.exceptions import ValidationError
from gerenciador_de_pedidos.serializers import PedidoSerializerResponse, PedidoSerializerRequest
import json

# Testes de models.py

# Testes de criação de pedido, representação em string, opções de status, método save, relacionamentos, campos nulos, queries complexas e muitos produtos
class PedidoModelTest(TestCase):
    def setUp(self):
        # Cria dados de teste que serão usados em vários testes
        self.cliente = Cliente.objects.create(
            nome="Maria Souza",
            telefone="11987654321",
            cep="13575140",
            logradouro="Rua João Ribeiro de Souza Filho",
            numero="123",
            bairro="Jardim Beatriz"      
        )
        self.funcionario = Funcionario.objects.create(
            nome="Carlos Oliveira",
            cpf="70541771850",
            email="carlos@example.com",
            usuario="carlos123",
            senha="senha123"
        )
        self.motoboy = Motoboy.objects.create(
            nome="João Silva",
            telefone="11999999999",
            placa="ABC1234",
            funcionario=self.funcionario,
            usuario="joao123",
            senha="senha123"
        )
        self.produto1 = Produto.objects.create(
            nome="Produto 1",
            preco=10.99
        )
        self.produto2 = Produto.objects.create(
            nome="Produto 2",
            preco=20.50
        )
        self.produto3 = Produto.objects.create(
            nome="Produto 3",
            preco=19.00
        )

        # Cria um pedido básico para testes
        self.pedido = Pedido.objects.create(
            cliente=self.cliente,
            funcionario=self.funcionario,
            motoboy=self.motoboy,
            data_hora_inicio=timezone.now(),
            status='em_andamento'
        )
        self.pedido.produtos.add(self.produto1, self.produto2)

    def test_criacao_pedido(self):
        # Testa a criação básica de um pedido
        self.assertEqual(self.pedido.status, 'em_andamento')
        self.assertIsNotNone(self.pedido.data_hora_inicio)
        self.assertIsNone(self.pedido.data_hora_finalizacao)
        self.assertEqual(self.pedido.produtos.count(), 2)

    def test_str_representation(self):
        # Testa a representação em string do modelo
        expected_str = f"Pedido iniciado em {self.pedido.data_hora_inicio} para {self.cliente}"
        self.assertEqual(str(self.pedido), expected_str)

    def test_status_choices(self):
        # Testa as opções de status disponíveis
        choices = dict(Pedido.STATUS_CHOICES)
        self.assertEqual(choices['em_andamento'], 'Em andamento')
        self.assertEqual(choices['entregue'], 'Entregue')
        self.assertEqual(choices['cancelado'], 'Cancelado')

    def test_save_method_em_andamento(self):
        # Testa o método save para status 'em_andamento'
        novo_pedido = Pedido(
            cliente=self.cliente,
            funcionario=self.funcionario,
            motoboy=self.motoboy,
            status='em_andamento'
        )
        novo_pedido.save()
        
        self.assertIsNotNone(novo_pedido.data_hora_inicio)
        self.assertIsNone(novo_pedido.data_hora_finalizacao)

    def test_save_method_entregue(self):
        # Testa o método save para status 'entregue'
        self.pedido.status = 'entregue'
        self.pedido.save()
        
        self.assertIsNotNone(self.pedido.data_hora_finalizacao)
        self.assertTrue(self.pedido.data_hora_finalizacao <= timezone.now())

    def test_save_method_cancelado(self):
        # Testa o método save para status 'cancelado'
        self.pedido.status = 'cancelado'
        self.pedido.save()
        
        self.assertIsNotNone(self.pedido.data_hora_finalizacao)
        self.assertTrue(self.pedido.data_hora_finalizacao <= timezone.now())

    def test_data_hora_inicio_manual(self):
        # Testa se é possível definir manualmente a data/hora de início
        data_manual = timezone.now() - timedelta(days=1)
        pedido = Pedido(
            cliente=self.cliente,
            funcionario=self.funcionario,
            motoboy=self.motoboy,
            status='em_andamento',
            data_hora_inicio=data_manual
        )
        pedido.save()
        
        self.assertEqual(pedido.data_hora_inicio, data_manual)

    def test_relacionamento_produtos(self):
        # Testa o relacionamento ManyToMany com Produto
        self.assertIn(self.produto1, self.pedido.produtos.all())
        self.assertIn(self.produto2, self.pedido.produtos.all())

    def test_relacionamento_cliente_null(self):
        # Testa se o cliente pode ser nulo
        pedido = Pedido.objects.create(
            funcionario=self.funcionario,
            motoboy=self.motoboy,
            status='em_andamento'
        )
        self.assertIsNone(pedido.cliente)

    def test_relacionamento_funcionario_null(self):
        # Testa se o funcionário pode ser nulo
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            motoboy=self.motoboy,
            status='em_andamento'
        )
        self.assertIsNone(pedido.funcionario)

    def test_relacionamento_motoboy_null(self):
        # Testa se o motoboy pode ser nulo
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            funcionario=self.funcionario,
            status='em_andamento'
        )
        self.assertIsNone(pedido.motoboy)

    def test_queryset_pedidos_em_andamento(self):
        em_andamento = Pedido.objects.filter(status='em_andamento')
        self.assertEqual(em_andamento.count(), 1)  # O pedido criado no setUp

    def test_muitos_produtos(self):
        for i in range(100):
            produto = Produto.objects.create(nome=f"Produto Massivo {i}", preco=i)
            self.pedido.produtos.add(produto)
        self.assertEqual(self.pedido.produtos.count(), 102)  # 2 do setUp + 100 novos

# Teste de serializers.py

# Testes de serialização e validação de dados, incluindo campos obrigatórios, representação legível, cálculo de total do pedido e serialização de produtos, cliente, funcionário e motoboy
class PedidoSerializerResponseTest(TestCase):

    def setUp(self):
        # Criação dos objetos necessários
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            telefone="11999999999",
            cep="00000000",
            logradouro="Rua Teste",
            numero="123",
            bairro="Bairro Teste"
        )
        
        self.funcionario = Funcionario.objects.create(
            nome="Funcionário Teste",
            cpf="12345678901",
            email="funcionario@teste.com",
            usuario="func_test",
            senha="senha123"
        )
        
        self.motoboy = Motoboy.objects.create(
            nome="Motoboy Teste",
            telefone="11988888888",
            placa="TEST123",
            funcionario=self.funcionario,
            usuario="moto_test",
            senha="senha123"
        )
        
        self.produto1 = Produto.objects.create(nome="Produto 1", preco=10.50)
        self.produto2 = Produto.objects.create(nome="Produto 2", preco=20.00)
        
        self.pedido = Pedido.objects.create(
            cliente=self.cliente,
            funcionario=self.funcionario,
            motoboy=self.motoboy,
            data_hora_inicio=timezone.now(),
            status='em_andamento'
        )
        self.pedido.produtos.add(self.produto1, self.produto2)

    def test_serializer_fields(self):
        # Testa se todos os campos estão presentes na serialização
        serializer = PedidoSerializerResponse(instance=self.pedido)
        data = serializer.data
        
        self.assertEqual(set(data.keys()), {
            'id', 'data_hora_inicio', 'data_hora_finalizacao', 
            'produtos', 'cliente', 'funcionario', 'motoboy', 
            'status', 'total_pedido'
        })

    def test_status_display(self):
        # Testa se o status está sendo convertido para a representação legível
        serializer = PedidoSerializerResponse(instance=self.pedido)
        self.assertEqual(serializer.data['status'], 'Em andamento')

    def test_total_pedido_calculation(self):
        # Testa o cálculo do total do pedido
        serializer = PedidoSerializerResponse(instance=self.pedido)
        expected_total = float(self.produto1.preco + self.produto2.preco)
        self.assertEqual(serializer.data['total_pedido'], expected_total)

    def test_produtos_serialization(self):
        # Testa se os produtos estão sendo serializados corretamente
        serializer = PedidoSerializerResponse(instance=self.pedido)
        self.assertEqual(len(serializer.data['produtos']), 2)
        self.assertEqual(serializer.data['produtos'][0]['nome'], 'Produto 1')
        self.assertEqual(serializer.data['produtos'][1]['nome'], 'Produto 2')

    def test_cliente_serialization(self):
        # Testa se o cliente está sendo serializado corretamente
        serializer = PedidoSerializerResponse(instance=self.pedido)
        self.assertEqual(serializer.data['cliente']['nome'], 'Cliente Teste')

    def test_funcionario_serialization(self):
        # Testa se o funcionário está sendo serializado corretamente
        serializer = PedidoSerializerResponse(instance=self.pedido)
        self.assertEqual(serializer.data['funcionario']['nome'], 'Funcionário Teste')

    def test_motoboy_serialization(self):
        # Testa se o motoboy está sendo serializado corretamente
        serializer = PedidoSerializerResponse(instance=self.pedido)
        self.assertEqual(serializer.data['motoboy']['nome'], 'Motoboy Teste')

    def test_data_hora_finalizacao_read_only(self):
        # Testa se data_hora_finalizacao é somente leitura
        serializer = PedidoSerializerResponse(instance=self.pedido)
        self.assertIsNone(serializer.data['data_hora_finalizacao'])
class PedidoSerializerRequestTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            telefone="11999999999",
            cep="00000000",
            logradouro="Rua Teste",
            numero="123",
            bairro="Bairro Teste"
        )
        
        self.funcionario = Funcionario.objects.create(
            nome="Funcionário Teste",
            cpf="12345678901",
            email="funcionario@teste.com",
            usuario="func_test",
            senha="senha123"
        )
        
        self.produto1 = Produto.objects.create(nome="Produto 1", preco=10.50)
        self.produto2 = Produto.objects.create(nome="Produto 2", preco=20.00)

    def test_create_pedido(self):
        # Testa a criação de um novo pedido
        data = {
            'produtos': [self.produto1.id, self.produto2.id],
            'cliente': self.cliente.id,
            'funcionario': self.funcionario.id
        }
        
        serializer = PedidoSerializerRequest(data=data)
        self.assertTrue(serializer.is_valid())
        
        pedido = serializer.save()
        self.assertIsNotNone(pedido.data_hora_inicio)
        self.assertEqual(pedido.produtos.count(), 2)
        self.assertEqual(pedido.cliente, self.cliente)
        self.assertEqual(pedido.funcionario, self.funcionario)

    def test_validate_funcionario_required(self):
        # Testa a validação do campo funcionario obrigatório
        data = {
            'produtos': [self.produto1.id],
            'cliente': self.cliente.id,
            'funcionario': None
        }
        
        serializer = PedidoSerializerRequest(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertIn('O campo \'funcionario\' é obrigatório.', str(context.exception))

    def test_serializer_fields(self):
        # Testa os campos do serializer de request
        serializer = PedidoSerializerRequest()
        self.assertEqual(set(serializer.fields.keys()), {'produtos', 'cliente', 'funcionario'})

class PedidoSerializerEdgeCasesTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            telefone="11999999999",
            cep="00000000",
            logradouro="Rua Teste",
            numero="123",
            bairro="Bairro Teste"
        )
        
        self.funcionario = Funcionario.objects.create(
            nome="Funcionário Teste",
            cpf="12345678901",
            email="funcionario@teste.com",
            usuario="func_test",
            senha="senha123"
        )

        self.motoboy = Motoboy.objects.create(
            nome="Motoboy Teste",
            telefone="11988888888",
            placa="TEST123",
            funcionario=self.funcionario,
            usuario="moto_test",
            senha="senha123"
        )
        
        self.produto1 = Produto.objects.create(nome="Produto 1", preco=10.50)
        self.produto2 = Produto.objects.create(nome="Produto 2", preco=20.00)
        
        self.pedido = Pedido.objects.create(
            cliente=self.cliente,
            funcionario=self.funcionario,
            motoboy=self.motoboy,
            data_hora_inicio=timezone.now(),
            status='em_andamento'
        )
        self.pedido.produtos.add(self.produto1, self.produto2)

    def test_empty_produtos_list(self):
        # Testa criação de pedido com lista vazia de produtos
        data = {
            'produtos': [],
            'cliente': self.cliente.id,
            'funcionario': self.funcionario.id
        }
        
        serializer = PedidoSerializerRequest(data=data)
        self.assertFalse(serializer.is_valid())
        
        self.assertIn('produtos', serializer.errors)

    def test_null_cliente(self):
        # Testa criação de pedido com cliente nulo
        data = {
            'produtos': [self.produto1.id],
            'cliente': None,
            'funcionario': self.funcionario.id
        }
        
        serializer = PedidoSerializerRequest(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('cliente', serializer.errors)
        self.assertEqual(serializer.errors['cliente'][0], "This field may not be null.")

    def test_total_pedido_zero(self):
        # Testa cálculo de total quando não há produtos
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            funcionario=self.funcionario,
            data_hora_inicio=timezone.now()
        )
        
        serializer = PedidoSerializerResponse(instance=pedido)
        self.assertEqual(serializer.data['total_pedido'], 0)


# Testes de urls.py

# Testes de views.py