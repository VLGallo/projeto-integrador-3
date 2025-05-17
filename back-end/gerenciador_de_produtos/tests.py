from django.test import TestCase
from django.core.exceptions import ValidationError
from gerenciador_de_produtos.models import Produto
from decimal import Decimal
from .serializers import ProdutoSerializer
from django.urls import resolve, reverse
from .views import (ProdutoView, ProdutoDetailView, ProdutoUpdateView, ProdutoDeleteView, ProdutoListView)
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.exceptions import NotFound

# Testes de models.py

# Verifica se o produto foi criado corretamente, se os campos obrigatórios estão funcionando, se o tamanho máximo do nome é respeitado, se o preço é positivo, se a constraint de unicidade está funcionando, o armazenamento de casas decimais e o limite de dígitos do preço.
class ProdutoModelTest(TestCase):
    
    def setUp(self):
        # Dados de teste reutilizáveis
        self.produto_data = {
            'nome': 'Marguerita',
            'preco': Decimal('29.90')
        }

    def test_criacao_produto_valido(self):
        # Testa a criação de um produto válido
        produto = Produto.objects.create(**self.produto_data)
        
        self.assertEqual(produto.nome, 'Marguerita')
        self.assertEqual(produto.preco, Decimal('29.90'))
        self.assertIsNotNone(produto.id)
        self.assertEqual(str(produto), 'Marguerita')  # Testa __str__

    def test_campos_obrigatorios(self):
        # Testa que nome e preço são obrigatórios
        # Teste para nome vazio
        produto = Produto(nome='', preco=Decimal('20.99'))
        with self.assertRaises(ValidationError):
            produto.full_clean()

        # Teste para preço ausente
        produto = Produto(nome='Produto Teste')
        with self.assertRaises(ValidationError):
            produto.full_clean()

    def test_tamanho_maximo_nome(self):
        # Testa o tamanho máximo do campo nome
        produto = Produto.objects.create(
            nome='A' * 201,  # Excede o máximo
            preco=Decimal('20.99')
        )
        with self.assertRaises(ValidationError):
            produto.full_clean()

    def test_preco_positivo(self):
        # Testa que o preço deve ser positivo
        with self.assertRaises(ValidationError):
            produto = Produto.objects.create(
                nome='Produto Inválido',
                preco=Decimal('-10.99')
            )
            produto.full_clean()

    def test_unique_constraint(self):
        # Testa a constraint de unicidade nome+preco
        Produto.objects.create(**self.produto_data)
        
        with self.assertRaises(Exception):  # Pode ser IntegrityError ou ValidationError
            Produto.objects.create(**self.produto_data)

    def test_preco_decimal_places(self):
        # Testa que o preço aceita 2 casas decimais
        produto = Produto.objects.create(
            nome='Produto Decimal',
            preco=Decimal('23.99')
        )
        self.assertEqual(produto.preco, Decimal('23.99'))

    def test_preco_max_digits(self):
        # Testa o limite de dígitos do preço
        # Teste com valor no limite (9999999.99 - 7+2=9 dígitos)
            produto = Produto(
                nome='Produto Caro',
                preco=Decimal('9999999.99')
            )
            produto.full_clean()  # Não deve levantar exceção

            # Teste com valor acima do limite (100000000.00 - 9+2=11 dígitos)
            produto = Produto(
                nome='Produto Muito Caro',
                preco=Decimal('100000000.00')
            )
            with self.assertRaises(ValidationError) as context:
                produto.full_clean()
            self.assertIn('Certifique-se de que não tenha mais de 10 dígitos no total.', str(context.exception))

            # Teste com muitos dígitos decimais (123.123456789 - 3+9=12 dígitos)
            produto = Produto(
                nome='Produto Decimal',
                preco=Decimal('123.123456789')
            )
            with self.assertRaises(ValidationError) as context:
                produto.full_clean()
            self.assertIn('Certifique-se de que não tenha mais de 10 dígitos no total.', str(context.exception))


# Teste de serializers.py

# Verifica se o serializer está funcionando corretamente, se todos os campos estão presentes, se a serialização de um produto existente está correta, se a criação de um novo produto com dados válidos funciona, se as validações de nome e preço estão corretas, se a constraint de unicidade está funcionando e se o limite de dígitos do preço é respeitado.
class ProdutoSerializerTest(TestCase):
    def setUp(self):
        self.produto_data = {
            'nome': 'Marguerita',
            'preco': '49.99'
        }
        self.produto = Produto.objects.create(
            nome='Calabresa',
            preco=Decimal('29.90')
        )

    def test_serializer_fields(self):
        # Testa se todos os campos estão presentes no serializer
        serializer = ProdutoSerializer()
        self.assertEqual(
            set(serializer.fields.keys()),
            {'id', 'nome', 'preco'}
        )

    def test_serialize_produto(self):
        #Testa a serialização de um produto existente
        serializer = ProdutoSerializer(self.produto)
        expected_data = {
            'id': self.produto.id,
            'nome': 'Calabresa',
            'preco': '29.90'
        }
        self.assertEqual(serializer.data, expected_data)

    def test_create_produto_valido(self):
        #Testa a criação de um novo produto com dados válidos
        serializer = ProdutoSerializer(data=self.produto_data)
        self.assertTrue(serializer.is_valid())
        produto = serializer.save()
        self.assertEqual(produto.nome, 'Marguerita')
        self.assertEqual(produto.preco, Decimal('49.99'))

    def test_validacao_nome_obrigatorio(self):
        #Testa que o nome é obrigatório
        data = {'preco': '40.00'}
        serializer = ProdutoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nome', serializer.errors)

    def test_validacao_preco_obrigatorio(self):
        #Testa que o preço é obrigatório
        data = {'nome': 'Lombo'}
        serializer = ProdutoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('preco', serializer.errors)

    def test_validacao_preco_positivo(self):
        #Testa que o preço deve ser positivo
        data = {'nome': 'Produto Inválido', 'preco': '-29.99'}
        serializer = ProdutoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('preco', serializer.errors)
        self.assertEqual(
            str(serializer.errors['preco'][0]),
            'Certifique-se que este valor seja maior ou igual a 0.01.'
        )

        #Teste com zero
        data = {'nome': 'Produto Zero', 'preco': '0.00'}
        serializer = ProdutoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('preco', serializer.errors)
        self.assertEqual(
            str(serializer.errors['preco'][0]),
            "Certifique-se que este valor seja maior ou igual a 0.01."
     )
        
        #Teste com valor positivo válido
        data = {'nome': 'Produto Válido', 'preco': '0.01'}
        serializer = ProdutoSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_validacao_preco_max_digits(self):
        #Testa o limite de dígitos do preço
        # 10 dígitos no total (incluindo decimais)
        data_valida = {'nome': 'Produto Caro', 'preco': '12345678.90'}  # 8+2=10 dígitos
        serializer = ProdutoSerializer(data=data_valida)
        self.assertTrue(serializer.is_valid())

        #Teste com valor acima do limite (11 dígitos)
        data_invalida = {'nome': 'Produto Muito Caro', 'preco': '123456789.01'}  # 9+2=11 dígitos
        serializer = ProdutoSerializer(data=data_invalida)
        self.assertFalse(serializer.is_valid())
        self.assertIn('preco', serializer.errors)
        self.assertEqual(
            str(serializer.errors['preco'][0]),
            "O preço não pode ter mais que 10 dígitos no total."
        )

    def test_validacao_nome_max_length(self):
        #Testa o tamanho máximo do campo nome
        data = {
            'nome': 'A' * 201,  # Excede o máximo de 200 caracteres
            'preco': '29.99'
        }
        serializer = ProdutoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nome', serializer.errors)

    def test_unique_constraint(self):
        #Testa a constraint de unicidade nome+preco
        # Cria primeiro produto
        data = {'nome': 'Produto Único', 'preco': '29.99'}
        serializer = ProdutoSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        # Tenta criar produto com mesmo nome e preço
        serializer = ProdutoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

# Testes urls.py

# Verifica se as URLs estão resolvendo corretamente para as views correspondentes, se os padrões de URL estão corretos e se todas as URLs foram definidas.
class ProdutosUrlsTest(TestCase):
    
    def test_produto_list_url_resolves(self):
        #Testa se a URL de listagem de produtos está correta
        url = reverse('produto-list')
        self.assertEqual(url, '/produto')
        self.assertEqual(resolve(url).func.view_class, ProdutoListView)

    def test_produto_add_url_resolves(self):
        #Testa se a URL de criação de produto está correta
        url = reverse('produto-add')
        self.assertEqual(url, '/produto/add')
        self.assertEqual(resolve(url).func.view_class, ProdutoView)

    def test_produto_detail_url_resolves(self):
        #Testa se a URL de detalhes de produto está correta
        url = reverse('produto-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/produto/1')
        self.assertEqual(resolve(url).func.view_class, ProdutoDetailView)

    def test_produto_update_url_resolves(self):
        #Testa se a URL de atualização de produto está correta
        url = reverse('produto-update', kwargs={'pk': 1})
        self.assertEqual(url, '/produto/update/1')
        self.assertEqual(resolve(url).func.view_class, ProdutoUpdateView)

    def test_produto_delete_url_resolves(self):
        #Testa se a URL de exclusão de produto está correta
        url = reverse('produto-delete', kwargs={'pk': 1})
        self.assertEqual(url, '/produto/delete/1')
        self.assertEqual(resolve(url).func.view_class, ProdutoDeleteView)

    def test_url_patterns_count(self):
        #Testa se todas as URLs foram definidas"
        from .urls import urlpatterns
        self.assertEqual(len(urlpatterns), 5)

# Testes de views.py

# Verifica se as views estão funcionando corretamente, se os métodos HTTP estão respondendo como esperado, se as respostas têm os códigos de status corretos, se os dados retornados estão corretos e se as exceções são tratadas adequadamente.
class ProdutoViewTest(TestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.produto_data = {
            'nome': 'Marguerita',
            'preco': '49.99'
        }
        self.existing_produto = Produto.objects.create(
            nome='Calabresa',
            preco=Decimal('29.90')
        )

    #Testes para ProdutoView (POST /produto/add/)
    
    def test_add_produto_success(self):
        #Testa criação de produto com dados válidos
        request = self.factory.post('/produto/add', self.produto_data)
        view = ProdutoView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 2)
        self.assertEqual(response.data['nome'], 'Marguerita')

    def test_add_produto_missing_fields(self):
        #Testa criação de produto com campos faltando
        data = {'nome': 'Produto Incompleto'}
        request = self.factory.post('/produto/add', data)
        view = ProdutoView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('preco', response.data)

    def test_add_duplicate_produto(self):
        #Testa tentativa de criar produto duplicado
        data = {'nome': 'Calabresa', 'preco': '29.90'}
        request = self.factory.post('/produto/add', data)
        view = ProdutoView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(
            str(response.data['non_field_errors'][0]), "The fields nome, preco must make a unique set.")

    # Testes para ProdutoListView (GET /produto/)
    
    def test_list_produtos(self):
        #Testa listagem de produtos
        request = self.factory.get('/produto')
        view = ProdutoListView.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], 'Calabresa')

    # Testes para ProdutoDetailView (GET /produto/<pk>/)
    
    def test_retrieve_produto(self):
        #Testa obtenção de detalhes de produto existente
        request = self.factory.get('/produto/1')
        view = ProdutoDetailView.as_view()
        response = view(request, pk=self.existing_produto.pk)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Calabresa')

    def test_retrieve_nonexistent_produto(self):
        #Testa obtenção de produto não existente
        request = self.factory.get('/produto/999')
        view = ProdutoDetailView.as_view()
        response = view(request, pk=999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Produto não encontrado")


    # Testes para ProdutoUpdateView (PUT /produto/update/<pk>/)
   
    def test_update_produto(self):
        #Testa atualização de produto existente
        data = {'nome': 'Lombo', 'preco': '39.90'}
        request = self.factory.put('/produto/update/1', data)
        view = ProdutoUpdateView.as_view()
        response = view(request, pk=self.existing_produto.pk)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Lombo')
        self.assertEqual(response.data['preco'], '39.90')

    def test_update_produto_invalid_data(self):
        #Testa atualização com dados inválidos
        data = {'nome': '', 'preco': '-10.00'}
        request = self.factory.put('/produto/update/1', data)
        view = ProdutoUpdateView.as_view()
        response = view(request, pk=self.existing_produto.pk)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('preco', response.data)

    # Testes para ProdutoDeleteView (DELETE /produto/delete/<pk>/)
    
    def test_delete_produto(self):
        #Testa exclusão de produto existente
        request = self.factory.delete('/produto/delete/1')
        view = ProdutoDeleteView.as_view()
        response = view(request, pk=self.existing_produto.pk)
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Produto.objects.count(), 0)

    def test_delete_nonexistent_produto(self):
        #Testa exclusão de produto não existente
        request = self.factory.delete('/produto/delete/999')
        view = ProdutoDeleteView.as_view()
        response = view(request, pk=999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Produto não encontrado")