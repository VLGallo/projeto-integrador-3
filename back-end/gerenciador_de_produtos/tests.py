from django.test import TestCase
from django.core.exceptions import ValidationError
from gerenciador_de_produtos.models import Produto
from decimal import Decimal

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