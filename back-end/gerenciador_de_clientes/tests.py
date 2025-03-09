from rest_framework.exceptions import ValidationError
from django.test import TestCase
from gerenciador_de_clientes.serializers import ClienteSerializer
from gerenciador_de_clientes.models import Cliente
from django.urls import reverse, resolve
from gerenciador_de_clientes.views import (
    ClienteListView, ClienteDetailView, ClienteView,
    ClienteUpdateView, ClienteDeleteView, BuscaCepView
)
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


#Teste de models.py

# Teste: criar um cliente válido, testar tamanho dos campos, testar se o complemento pode ser vazio, testar valores válidos, verificar a restrição de unicidade (unique_cliente) e testar a conversão para string (__str_)

class ClienteModelTest(TestCase):
    
    def setUp(self):
        # Configura um cliente antes de cada teste
        self.cliente = Cliente.objects.create(
            nome="João da Silva",
            telefone="11987654321",
            cep="12345678",
            logradouro="Rua A",
            numero="123",
            complemento="Apto 10",
            bairro="Centro"
        )

    def test_max_length_nome(self):
        # Testa o campo 'nome' com max_length=200
        cliente = Cliente(nome='A' * 201) # Tenta criar um nome com 201 caracteres
        with self.assertRaises(Exception): # Espera-se que uma exceção seja levantada
            cliente.full_clean() # Valida o modelo

    def test_max_length_telefone(self):
        # Testa o campo 'telefone' com max_length=215
        cliente = Cliente(telefone='1' * 16) # Tenta criar um telefone com 16 caracteres
        with self.assertRaises(Exception): # Espera-se que uma exceção seja levantada
            cliente.full_clean() # Valida o modelo

    def test_max_length_cep(self):
        # Testa o campo 'cep' com max_length=8
        cliente = Cliente(cep='2' * 9) # Tenta criar um cep com 9 caracteres
        with self.assertRaises(Exception): # Espera-se que uma exceção seja levantada
            cliente.full_clean() # Valida o modelo

    def test_max_length_logradouro(self):
        # Testa o campo 'logradouro' com max_length=200
        cliente = Cliente(logradouro='A' * 201) # Tenta criar um logradouro com 201 caracteres
        with self.assertRaises(Exception): # Espera-se que uma exceção seja levantada
            cliente.full_clean() # Valida o modelo

    def test_max_length_numero(self):
        # Testa o campo 'numero' com max_length=10
        cliente = Cliente(numero='3' * 11) # Tenta criar um numero com 11 caracteres
        with self.assertRaises(Exception): # Espera-se que uma exceção seja levantada
            cliente.full_clean() # Valida o modelo

    def test_max_length_complemento(self):
        # Testa o campo 'complemento' com max_length=30
        cliente = Cliente(complemento='B' * 31) # Tenta criar um complemento com 31 caracteres
        with self.assertRaises(Exception): # Espera-se que uma exceção seja levantada
            cliente.full_clean() # Valida o modelo    

    def test_max_length_bairro(self):
        # Testa o campo 'bairro' com max_length=200
        cliente = Cliente(bairro='C' * 201) # Tenta criar um bairro com 201 caracteres
        with self.assertRaises(Exception): # Espera-se que uma exceção seja levantada
            cliente.full_clean() # Valida o modelo    

    def test_complemento_null_and_blank(self):
        # Testa se o campo 'complemento' pode ser nulo ou em branco
        cliente = Cliente(
            nome='João da Silva',
            telefone='11987654321',
            cep='12345678',
            logradouro='Rua A',
            numero='123',
            bairro='Centro',
            complemento=None  # Campo pode ser nulo
        )
        cliente.full_clean()  # Valida o modelo (não deve levantar exceção)

        cliente.complemento = ''  # Campo pode ser em branco
        cliente.full_clean()  # Valida o modelo (não deve levantar exceção)
   
    def test_criacao_cliente(self):
        # Verifica se o cliente foi criado corretamente
        cliente = Cliente.objects.get(nome="João da Silva")
        self.assertEqual(cliente.telefone, "11987654321")
        self.assertEqual(cliente.cep, "12345678")
        self.assertEqual(cliente.logradouro, "Rua A")
        self.assertEqual(cliente.numero, "123")
        self.assertEqual(cliente.complemento, "Apto 10")
        self.assertEqual(cliente.bairro, "Centro")

    def test_constraint_unique_cliente(self):
        # Verifica se a restrição de unicidade impede clientes duplicados
        with self.assertRaises(Exception):
            Cliente.objects.create(
                nome="João da Silva",
                telefone="11987654321",
                cep="12345678",
                logradouro="Rua A",
                numero="123",
                complemento="Apto 10",
                bairro="Centro"
            )

    def test_str_representation(self):
        # Verifica se o método __str__ retorna corretamente o nome do cliente
        cliente = Cliente(nome='João da Silva')
        self.assertEqual(str(self.cliente), "João da Silva")

    def test_valid_values(self):
        # Teste para valores válidos
        cliente = Cliente(
            nome='João da Silva',
            telefone='11987654321',
            cep='12345678',
            logradouro='Rua A',
            numero='123',
            bairro='Centro',
            complemento='Apto 101'
        )
        cliente.full_clean()   # Valida o modelo (não deve levantar exceção)

# Teste de serializers.py

# Teste: Validação do telefone (remove caracteres especiais, remove zero extra antes do DDD, bloqueia números muito curtos ou longos), serialização e desserialização (garante que os dados são serializados corretamente), campos obrigatórios (não permite campos obrigatórios vazios), máximos e mínimos de caracteres (bloqueia valores que ultrapassam o limite)

class ClienteSerializerTest(TestCase):

    def setUp(self):
        #Cria um cliente válido para os testes
        self.valid_data = {
            "nome": "João da Silva",
            "telefone": "11987654321",
            "cep": "12345678",
            "logradouro": "Rua B",
            "numero": "123",
            "complemento": "Apto 101",
            "bairro": "Centro"
        }

    def test_serialization(self):
        #Testa se a serialização de um cliente funciona corretamente
        cliente = Cliente.objects.create(**self.valid_data)
        serializer = ClienteSerializer(cliente)
        self.assertEqual(serializer.data["nome"], "João da Silva")
        self.assertEqual(serializer.data["telefone"], "11987654321")

    def test_valid_desserialization(self):
        #Testa a desserialização de dados válidos
        serializer = ClienteSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_required_fields(self):
        #Testa se os campos obrigatórios estão realmente sendo validados
        required_fields = ["nome", "telefone", "cep", "logradouro", "numero", "bairro"]
        for field in required_fields:
            data = self.valid_data.copy()
            data.pop(field)  # Remove o campo a ser testado
            serializer = ClienteSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

    def test_telefone_limpo(self):
        #Testa se o telefone é limpo corretamente, removendo caracteres especiais
        data = self.valid_data.copy()
        data["telefone"] = "(11) 98765-4321"
        serializer = ClienteSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["telefone"], "11987654321")

    def test_telefone_com_zero_no_ddd(self):
        #Testa se um telefone com zero antes do DDD é tratado corretamente
        data = self.valid_data.copy()
        data["telefone"] = "011987654321"
        serializer = ClienteSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["telefone"], "11987654321")

    def test_telefone_curto(self):
        #Testa um telefone com menos de 10 dígitos
        data = self.valid_data.copy()
        data["telefone"] = "9876543"
        serializer = ClienteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("telefone", serializer.errors)

    def test_telefone_longo(self):
        #Testa um telefone com mais de 11 dígitos
        data = self.valid_data.copy()
        data["telefone"] = "55119876543210"
        serializer = ClienteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("telefone", serializer.errors)

    def test_max_length_fields(self):
        #Testa se os campos respeitam os limites de caracteres
        max_lengths = {
            "nome": 200,
            "telefone": 15,  # 11 é o normal, mas alguns bancos podem armazenar com +55
            "cep": 8,
            "logradouro": 200,
            "numero": 10,
            "complemento": 30,
            "bairro": 200,
        }
        for field, max_length in max_lengths.items():
            data = self.valid_data.copy()
            data[field] = "A" * (max_length + 1)  # Insere 1 caractere a mais
            serializer = ClienteSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

    def test_valid_max_lengths(self):
        #Testa se os valores no limite máximo são aceitos
        max_lengths = {
            "nome": 200,
            "telefone": 11,
            "cep": 8,
            "logradouro": 200,
            "numero": 10,
            "complemento": 30,
            "bairro": 200,
        }
        for field, max_length in max_lengths.items():
            data = self.valid_data.copy()
            # Garante que o telefone seja um número válido no limite máximo
            if field == "telefone":
                data[field] = "9" * max_length  
            else:
                data[field] = "A" * max_lengths[field]  # Pega o valor correto do dicionário

            serializer = ClienteSerializer(data=data)
            self.assertTrue(serializer.is_valid(), serializer.errors)

    # Teste de urls.py

    # Teste: se urls existem e retornam os status HTTP corretos, se cada url resolve a view correta, se a url gera o caminho esperado quando chamada por reverse()

class ClienteUrlsTest(TestCase):

    # Testes de resolução (resolve()): verificam se a url definida no urlpatterns realmente chama a view correta.
    def test_cliente_list_url_resolves(self):
        url = "/cliente"
        self.assertEqual(resolve(url).func.view_class, ClienteListView)

    def test_cliente_add_url_resolves(self):
        url = "/cliente/add"
        self.assertEqual(resolve(url).func.view_class, ClienteView)

    def test_cliente_detail_url_resolves(self):
        url = "/cliente/1"
        self.assertEqual(resolve(url).func.view_class, ClienteDetailView)

    def test_cliente_update_url_resolves(self):
        url = "/cliente/update/1"
        self.assertEqual(resolve(url).func.view_class, ClienteUpdateView)

    def test_cliente_delete_url_resolves(self):
        url = "/cliente/delete/1"
        self.assertEqual(resolve(url).func.view_class, ClienteDeleteView)

    def test_busca_cep_url_resolves(self):
        url = "/buscacep/12345678/"
        self.assertEqual(resolve(url).func.view_class, BuscaCepView)

    # Testes de reverse(): Garantem que os nomes das urls retornam os caminhos corretos quando utilizados em templates ou chamadas de API.
    def test_cliente_list_reverse_url(self):
        url = reverse("cliente_list")
        self.assertEqual(url, "/cliente")

    def test_cliente_add_reverse_url(self):
        url = reverse("cliente_add")
        self.assertEqual(url, "/cliente/add")

    def test_cliente_detail_reverse_url(self):
        url = reverse("cliente_detail", args=[1])
        self.assertEqual(url, "/cliente/1")

    def test_cliente_update_reverse_url(self):
        url = reverse("cliente_update", args=[1])
        self.assertEqual(url, "/cliente/update/1")

    def test_cliente_delete_reverse_url(self):
        url = reverse("cliente_delete", args=[1])
        self.assertEqual(url, "/cliente/delete/1")

    def test_busca_cep_reverse_url(self):
        url = reverse("busca_cep", args=["12345678"])
        self.assertEqual(url, "/buscacep/12345678/")

    # Teste de views.py

    # Testa os principais fluxos da API, incluindo criação, listagem, busca, atualização e remoção de clientes, além da funcionalidade de busca de CEP.

class ClienteAPITestCase(APITestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="João Silva",
            telefone="11999999999",
            cep="01001000",
            logradouro="Praça da Sé",
            numero="1",
            complemento="",
            bairro="Sé"
        )
        self.valid_payload = {
            "nome": "Maria Souza",
            "telefone": "11988888888",
            "cep": "02020000",
            "logradouro": "Rua Teste",
            "numero": "100",
            "bairro": "Centro"
        }
  
    # Testa a criação bem-sucedida de um cliente
    def test_create_cliente_success(self):
        url = reverse("cliente_add")
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)

    # Testa se a API retorna erro ao tentar criar um cliente sem preencher todos os campos obrigatórios
    def test_create_cliente_missing_fields(self):
        url = reverse("cliente_add")
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # Testa a listagem de clientes cadastrados
    def test_list_clientes(self):
        url = reverse("cliente_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Testa se a API retorna corretamente os detalhes de um cliente específico
    def test_get_cliente_detail_success(self):
        url = reverse("cliente_detail", kwargs={"pk": self.cliente.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], self.cliente.nome)

    # Testa o comportamento ao tentar buscar um cliente inexistente
    def test_get_cliente_detail_not_found(self):
        url = reverse("cliente_detail", kwargs={"pk": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Testa a atualização de um cliente existente
    def test_update_cliente_success(self):
        url = reverse("cliente_update", kwargs={"pk": self.cliente.id})
        response = self.client.put(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nome, "Maria Souza")

    # Testa se a API retorna erro ao tentar atualizar um cliente inexistente
    def test_update_cliente_not_found(self):
        url = reverse("cliente_update", kwargs={"pk": 999})
        response = self.client.put(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Testa a exclusão de um cliente existente
    def test_delete_cliente_success(self):
        url = reverse("cliente_delete", kwargs={"pk": self.cliente.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cliente.objects.filter(id=self.cliente.id).exists())

    # Testa a tentativa de exclusão de um cliente inexistente
    def test_delete_cliente_not_found(self):
        url = reverse("cliente_delete", kwargs={"pk": 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Testa se a API de busca de CEP retorna os dados corretamente
    def test_busca_cep_success(self):
        url = reverse("busca_cep", kwargs={"cep": "01001000"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("logradouro", response.data)

    # Testa o comportamento da API ao buscar um CEP inválido
    def test_busca_cep_invalid(self):
        url = reverse("busca_cep", kwargs={"cep": "00000000"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # Testes adicionais