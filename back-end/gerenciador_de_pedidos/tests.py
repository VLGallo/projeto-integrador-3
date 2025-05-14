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
from django.urls import reverse, resolve
from .views import (PedidoView, PedidoListView, PedidoDetailView, PedidoUpdateView, PedidoDeleteView, PedidoAssignMotoboyView, PedidoActionView, PedidosAtribuidosMotoboysView)
from gerenciador_de_motoboys.views import PedidosMotoboyView
from datetime import datetime, date
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.exceptions import NotFound
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

# Verifica se as URLs estão resolvendo corretamente para as views correspondentes
class PedidosUrlsTest(TestCase):
    
    def test_pedido_list_url_resolves(self):
        #Verifica a URL de listagem de pedidos
        url = reverse('pedido-list')
        self.assertEqual(url, '/pedido')
        self.assertEqual(resolve(url).func.view_class, PedidoListView)

    def test_pedido_add_url_resolves(self):
        #Verifica a URL de criação de pedido
        url = reverse('pedido-add')
        self.assertEqual(url, '/pedido/add')
        self.assertEqual(resolve(url).func.view_class, PedidoView)

    def test_pedido_detail_url_resolves(self):
        #Verifica a URL de detalhes do pedido
        url = reverse('pedido-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/pedido/1')
        self.assertEqual(resolve(url).func.view_class, PedidoDetailView)

    def test_pedido_update_url_resolves(self):
        #Verifica a URL de atualização do pedido
        url = reverse('pedido-update', kwargs={'pk': 1})
        self.assertEqual(url, '/pedido/update/1')
        self.assertEqual(resolve(url).func.view_class, PedidoUpdateView)

    def test_pedido_delete_url_resolves(self):
        #Verifica a URL de exclusão do pedido
        url = reverse('pedido-delete', kwargs={'pk': 1})
        self.assertEqual(url, '/pedido/delete/1')
        self.assertEqual(resolve(url).func.view_class, PedidoDeleteView)

    def test_pedido_assign_motoboy_url_resolves(self):
        #Verifica a URL para atribuir motoboy ao pedido
        url = reverse('pedido-atribuir-motoboy', kwargs={'pk': 1, 'motoboy_id': 2})
        self.assertEqual(url, '/pedido/1/atribuir-motoboy/2')
        self.assertEqual(resolve(url).func.view_class, PedidoAssignMotoboyView)

    def test_pedido_action_url_resolves(self):
        #Verifica a URL para ações no pedido
        url = reverse('pedido-action', kwargs={'pk': 1, 'action': 'finalizar'})
        self.assertEqual(url, '/pedido/1/action/finalizar')
        self.assertEqual(resolve(url).func.view_class, PedidoActionView)

    def test_pedidos_motoboys_url_resolves(self):
        #Verifica a URL de pedidos atribuídos a motoboys
        url = reverse('pedidos-atribuidos-motoboys')
        self.assertEqual(url, '/pedido/motoboys')
        self.assertEqual(resolve(url).func.view_class, PedidosAtribuidosMotoboysView)

    def test_pedidos_motoboy_url_resolves(self):
        #Verifica a URL de pedidos de um motoboy específico
        url = reverse('pedidos-motoboy', kwargs={'motoboy_id': 1})
        self.assertEqual(url, '/pedido/motoboy/1')
        self.assertEqual(resolve(url).func.view_class, PedidosMotoboyView)

    def test_url_patterns_count(self):
        #Verifica se todas as URLs foram definidas
        from .urls import urlpatterns
        self.assertEqual(len(urlpatterns), 9)


# Testes de views.py

# Verifica a criação, listagem, detalhamento, atualização, exclusão, atribuição de motoboy e ações em pedidos

class PedidoViewTest(TestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()    

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

        self.pedido = Pedido.objects.create(
            cliente=self.cliente,
            funcionario=self.funcionario,
            motoboy=self.motoboy,
            data_hora_inicio=timezone.now(),
            status='em_andamento',
        )
        self.pedido.produtos.add(self.produto1, self.produto2)

        # Cria um pedido básico para testes
        self.pedidodata = {
            'cliente':self.cliente.id,
            'funcionario':self.funcionario.id,
            'motoboy':self.motoboy.id,
            'data_hora_inicio':timezone.now().isoformat(),
            'status':'em_andamento',
            'produtos':[self.produto1.id, self.produto2.id]
        } 

    # Testes para PedidoView (POST /pedido/add/)
    
    def test_create_pedido_success(self):
        #Testa criação de pedido com dados válidos
        request = self.factory.post('/pedido/add', self.pedidodata, format='json')
        view = PedidoView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pedido.objects.count(), 2)

    def test_create_pedido_missing_fields(self):
        #Testa criação de pedido com campos faltando
        data = {'cliente': self.cliente.id}  # Faltando funcionario
        request = self.factory.post('/pedido/add', data, format='json')
        view = PedidoView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('funcionario', response.data)

    def test_create_pedido_invalid_funcionario(self):
        #Testa criação de pedido com funcionário inválido
        data = {'cliente': self.cliente.id, 'funcionario': 999}
        request = self.factory.post('/pedido/add', data, format='json')
        view = PedidoView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('funcionario', response.data)

    # Testes para PedidoListView (GET /pedido/)

    def test_list_pedidos(self):
        #Testa listagem de pedidos
        request = self.factory.get('/pedido')
        view = PedidoListView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Testes para PedidoDetailView (GET /pedido/<pk>/)

    def test_retrieve_pedido(self):
        #Testa obtenção de detalhes de pedido existente
        request = self.factory.get('/pedido/1')
        view = PedidoDetailView.as_view()
        response = view(request, pk=self.pedido.pk)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cliente']['id'], self.cliente.id)

    def test_retrieve_nonexistent_pedido(self):
        #Testa obtenção de pedido não existente
        request = self.factory.get('/pedido/999')
        view = PedidoDetailView.as_view()
        response = view(request, pk=999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Testes para PedidoUpdateView (PUT /pedido/update/<pk>/)
    def test_update_pedido_status(self):
        #Testa atualização de status do pedido
        data = {'status': 'entregue'}
        request = self.factory.put('/pedido/update/1', data, format='json')
        view = PedidoUpdateView.as_view()
        response = view(request, pk=self.pedido.pk)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Status do pedido atualizado com sucesso")

    def test_update_pedido_invalid_status(self):
        #Testa atualização com status inválido
        data = {'status': 'invalido'}
        request = self.factory.put('/pedido/update/1', data, format='json')
        view = PedidoUpdateView.as_view()
        response = view(request, pk=self.pedido.pk)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testes para PedidoDeleteView (DELETE /pedido/delete/<pk>/)

    def test_delete_pedido(self):
        #Testa exclusão de pedido existente
        request = self.factory.delete('/pedido/delete/1')
        view = PedidoDeleteView.as_view()
        response = view(request, pk=self.pedido.pk)
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_delete_pedido_no_funcionario(self):
        #Testa exclusão de pedido sem funcionário associado
        pedido = Pedido.objects.create(cliente=self.cliente)

        request = self.factory.delete('/pedido/delete/1')
        view = PedidoDeleteView.as_view()
        response = view(request, pk=pedido.pk)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testes para PedidoAssignMotoboyView (PUT /pedido/<pk>/atribuir-motoboy/<motoboy_id>/)

    def test_assign_motoboy(self):
        # Testa atribuição de motoboy ao pedido
        request = self.factory.put('/pedido/1/atribuir-motoboy/1')
        view = PedidoAssignMotoboyView.as_view()
        response = view(request, pk=self.pedido.pk, motoboy_id=self.motoboy.pk)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['motoboy']['id'], self.motoboy.pk)

    def test_assign_nonexistent_motoboy(self):
        #Testa atribuição de motoboy inexistente
        request = self.factory.put('/pedido/1/atribuir-motoboy/999')
        view = PedidoAssignMotoboyView.as_view()
        response = view(request, pk=self.pedido.pk, motoboy_id=999)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testes para PedidoActionView (POST /pedido/<pk>/action/<action>/)

    def test_pedido_action_entregar(self):
        #Testa ação de entregar pedido
        request = self.factory.post('/pedido/1/action/entregar')
        view = PedidoActionView.as_view()
        response = view(request, pk=self.pedido.pk, action='entregar')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'entregue')

    def test_pedido_action_invalid(self):
        #Testa ação inválida no pedido
        request = self.factory.post('/pedido/1/action/invalido')
        view = PedidoActionView.as_view()
        response = view(request, pk=self.pedido.pk, action='invalido')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testes para PedidosMotoboyView (GET /pedido/motoboy/<motoboy_id>/)

    def test_pedidos_motoboy(self):
        #Testa listagem de pedidos por motoboy
        self.pedido.motoboy = self.motoboy
        self.pedido.save()
        
        request = self.factory.get('/pedido/motoboy/1')
        view = PedidosMotoboyView.as_view()
        response = view(request, motoboy_id=self.motoboy.pk)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Testes para PedidosAtribuidosMotoboysView (GET /pedido/motoboys/)

    def test_pedidos_motoboys(self):
        #Testa listagem de pedidos por motoboys
        self.pedido.motoboy = self.motoboy
        self.pedido.save()
        
        request = self.factory.get('/pedido/motoboys')
        view = PedidosAtribuidosMotoboysView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)