from django.test import TestCase, Client
from gerenciador_de_motoboys.serializers import MotoboySerializerRequest, MotoboySerializerResponse
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.urls import reverse
from gerenciador_de_motoboys.models import Motoboy
from gerenciador_de_funcionarios.models import Funcionario
from gerenciador_de_pedidos.models import Pedido
from gerenciador_de_clientes.models import Cliente
from gerenciador_de_produtos.models import Produto
from django.utils import timezone
import json


#Teste de models.py

#Teste: criar um motoboy válido, testar se os campos nome, telefone e placa são únicos, testar o preenchimento de campos obrigatórios, testar o relacionamento com o modelo funcionario e a conversão para sting (_str_)

class MotoboyModelTest(TestCase):
    
    def setUp(self):
        #Configura dados iniciais para os testes.
        self.funcionario = Funcionario.objects.create(
            nome="Victor Correa",
            cpf="697.023.938-17",
            email="victor.correa@gmail.com",
            usuario= "victorcorrea",
            senha="senha123"
        )

    def test_create_motoboy(self):
        #Testa a criação de um Motoboy com todos os campos.
        motoboy = Motoboy.objects.create(
            nome="João Silva",
            telefone="11987654321",
            placa="XYZ1O34",
            funcionario=self.funcionario,
            usuario="joao123",
            senha="senha123"
        )

        # Verifica se o objeto foi criado corretamente
        self.assertEqual(motoboy.nome, "João Silva")
        self.assertEqual(motoboy.telefone, "11987654321")
        self.assertEqual(motoboy.placa, "XYZ1O34")
        self.assertEqual(motoboy.funcionario, self.funcionario)
        self.assertEqual(motoboy.usuario, "joao123")
        self.assertEqual(motoboy.senha, "senha123")

    def test_create_motoboy_with_default_usuario_and_senha(self):
        #Testa a criação de um Motoboy sem fornecer usuário e senha.
        motoboy = Motoboy.objects.create(
            nome="Maria Souza",
            telefone="11999999999",
            placa="ABC5F78",
            funcionario=self.funcionario
        )

        # Verifica se os valores padrão foram atribuídos
        self.assertEqual(motoboy.usuario, "default_usuario")
        self.assertEqual(motoboy.senha, "default_senha")

    def test_unique_motoboy_constraint(self):
        #Testa a restrição de unicidade (nome, telefone, placa).
        # Cria o primeiro motoboy
        Motoboy.objects.create(
            nome="Carlos Oliveira",
            telefone="11988888888",
            placa="DEF9R12",
            funcionario=self.funcionario
        )

        # Tenta criar um segundo motoboy com os mesmos dados
        with self.assertRaises(Exception):
            Motoboy.objects.create(
                nome="Carlos Oliveira",
                telefone="11988888888",
                placa="DEF9R12",
                funcionario=self.funcionario
            )

    def test_motoboy_str_representation(self):
        #Testa a representação em string do modelo Motoboy.
        motoboy = Motoboy.objects.create(
            nome="Ana Costa",
            telefone="11977777777",
            placa="GHI3V56",
            funcionario=self.funcionario
        )

        # Verifica se o método __str__ retorna o nome do motoboy
        self.assertEqual(str(motoboy), "Ana Costa")

    def test_motoboy_without_funcionario(self):
        #Testa a criação de um Motoboy sem associar a um Funcionario.
        motoboy = Motoboy.objects.create(
            nome="Pedro Alves",
            telefone="11966666666",
            placa="JKL7L90"
        )

        # Verifica se o motoboy foi criado sem funcionário
        self.assertIsNone(motoboy.funcionario)

class MotoboyFieldSizeTests(TestCase):
    
    def setUp(self):
        #Configura dados iniciais para os testes.
        self.funcionario = Funcionario.objects.create(
            nome="Victor Correa",
            cpf="697.023.938-17",
            email="victor.correa@gmail.com",
            usuario= "victorcorrea",
            senha="senha123"
        )

    def test_valid_max_lengths(self):
        #Testa se os valores no limite máximo de tamanho são aceitos para cada campo.
        # Dados válidos para o Motoboy
        valid_data = {
            "nome": "João Silva",
            "telefone": "11987654321",
            "placa": "XYZ1D34",
            "usuario": "joao123",
            "senha": "senha123",
            "funcionario": self.funcionario.id
        }

        # Limites máximos de tamanho para cada campo (conforme definido no models.py)
        max_lengths = {
            "nome": 200,      # CharField(max_length=200)
            "telefone": 11,   # CharField(max_length=30) mas no serializers.py determina que o campo deve ter no máximo 11 caracteres
            "placa": 7,      # CharField(max_length=20) mas no serializers.py determina que o campo deve ter 7 caracteres
            "usuario": 100,   # CharField(max_length=100)
            "senha": 255,     # CharField(max_length=255)
        }

        for field, max_length in max_lengths.items():
            # Cria uma cópia dos dados válidos
            data = valid_data.copy()

            # Define o valor do campo no limite máximo
            if field == "telefone":
                # Telefone deve ter exatamente 11 dígitos (após limpeza)
                data[field] = "11987654321"  # Telefone válido com 11 dígitos
            elif field == "placa":
                # Placa deve ter exatamente 7 caracteres
                data[field] = "XYZ1234"  # Placa válida com 7 caracteres
            else:
                data[field] = "A" * max_length  # Preenche o campo com "A" até o limite máximo

            # Cria o serializer com os dados
            serializer = MotoboySerializerRequest(data=data)

            # Verifica se o serializer é válido
            self.assertTrue(serializer.is_valid(), f"Campo {field} falhou: {serializer.errors}")

    def test_invalid_max_lengths(self):
        #Testa se os valores acima do limite máximo de tamanho são rejeitados.
        # Dados válidos para o Motoboy
        valid_data = {
            "nome": "João Silva",
            "telefone": "11987654321",
            "placa": "XYZ1D34",
            "usuario": "joao123",
            "senha": "senha123",
            "funcionario": self.funcionario.id
        }

        # Limites máximos de tamanho para cada campo (conforme definido no models.py)
        max_lengths = {
            "nome": 200,      # CharField(max_length=200)
            "telefone": 11,   # CharField(max_length=30) mas no serializers.py determina que o campo deve ter no máximo 11 caracteres
            "placa": 7,      # CharField(max_length=20) mas no serializers.py determina que o campo deve ter 7 caracteres
            "usuario": 100,   # CharField(max_length=100)
            "senha": 255,     # CharField(max_length=255)
        }

        for field, max_length in max_lengths.items():
            # Cria uma cópia dos dados válidos
            data = valid_data.copy()

            # Define o valor do campo acima do limite máximo
            if field == "telefone":
                # Telefone inválido com 12 dígitos (acima do limite)
                data[field] = "119876543210"  # Telefone inválido com 12 dígitos
            elif field == "placa":
                # Placa inválida com 8 caracteres (acima do limite)
                data[field] = "XYZ12345"  # Placa inválida com 8 caracteres
            else:
                data[field] = "A" * (max_length + 1)  # Excede o limite máximo em 1 caractere

            # Cria o serializer com os dados
            serializer = MotoboySerializerRequest(data=data)

            # Verifica se o serializer é inválido
            self.assertFalse(serializer.is_valid(), f"Campo {field} deveria falhar: {serializer.errors}")
            self.assertIn(field, serializer.errors)  # Verifica se o erro está no campo esperado

#Teste de serializers.py

#Teste: validação de campos (telefone, placa, usuario, senha) e campos obrigatórios, serialização e desserialização, comportamento do serializer (create, update) e o MotoboySerilizersResponse.

class MotoboySerializerRequestTest(TestCase):
    
    def setUp(self):
        #Configura dados iniciais para os testes.

        #Cria um funcionário para ser usado nos testes
        self.funcionario = Funcionario.objects.create(
            nome="Victor Correa",
            cpf="697.023.938-17",
            email="victor.correa@gmail.com",
            usuario= "victorcorrea",
            senha="senha123"
        )

    def test_valid_data(self):
        #Testa se o serializer é válido com dados corretos.
        data = {
            "nome": "João Silva",
            "telefone": "11987654321",
            "placa": "XYZ1234",
            "usuario": "joao123",
            "senha": "senha123",
            "funcionario": self.funcionario.id
        }

        serializer = MotoboySerializerRequest(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_telefone(self):
        #Testa se o serializer rejeita telefones inválidos.
       
        #Telefone com menos de 10 dígitos
        data = {
            "nome": "João Silva",
            "telefone": "123456789",  # Inválido (9 dígitos)
            "placa": "XYZ1234",
            "usuario": "joao123",
            "senha": "senha123",
            "funcionario": self.funcionario.id
        }

        serializer = MotoboySerializerRequest(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("telefone", serializer.errors)

        #Telefone com mais de 11 dígitos
        data["telefone"] = "1198765432101"  # Inválido (12 dígitos)
        serializer = MotoboySerializerRequest(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("telefone", serializer.errors)

    def test_invalid_placa(self):
        #Testa se o serializer rejeita placas inválidas.
        
        #Placa com menos de 7 caracteres
        data = {
            "nome": "João Silva",
            "telefone": "11987654321",
            "placa": "XYZ12",  # Inválido (5 caracteres)
            "usuario": "joao123",
            "senha": "senha123",
            "funcionario": self.funcionario.id
        }

        serializer = MotoboySerializerRequest(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("placa", serializer.errors)

        #Placa com mais de 7 caracteres
        data["placa"] = "XYZ12345"  # Inválido (8 caracteres)
        
        serializer = MotoboySerializerRequest(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("placa", serializer.errors)

    def test_empty_usuario(self):
        #Testa se o serializer rejeita um usuário vazio.
        data = {
            "nome": "João Silva",
            "telefone": "11987654321",
            "placa": "XYZ1234",
            "usuario": "",  # Inválido (vazio)
            "senha": "senha123",
            "funcionario": self.funcionario.id
        }

        serializer = MotoboySerializerRequest(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("usuario", serializer.errors)

    def test_empty_senha(self):
        #Testa se o serializer rejeita uma senha vazia.
        data = {
            "nome": "João Silva",
            "telefone": "11987654321",
            "placa": "XYZ1234",
            "usuario": "joao123",
            "senha": "",  # Inválido (vazio)
            "funcionario": self.funcionario.id
        }

        serializer = MotoboySerializerRequest(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("senha", serializer.errors)

    def test_create_motoboy(self):
        #Testa se o método create cria um Motoboy corretamente.
        data = {
            "nome": "João Silva",
            "telefone": "11987654321",
            "placa": "XYZ1234",
            "usuario": "joao123",
            "senha": "senha123",
            "funcionario": self.funcionario.id
        }

        serializer = MotoboySerializerRequest(data=data)
        self.assertTrue(serializer.is_valid())

        motoboy = serializer.save()
        self.assertEqual(motoboy.nome, "João Silva")
        self.assertEqual(motoboy.telefone, "11987654321")
        self.assertEqual(motoboy.placa, "XYZ1234")
        self.assertEqual(motoboy.usuario, "joao123")
        self.assertEqual(motoboy.senha, "senha123")
        self.assertEqual(motoboy.funcionario, self.funcionario)

    def test_update_motoboy(self):
        #Testa se o método update atualiza um Motoboy corretamente.
        motoboy = Motoboy.objects.create(
            nome="João Silva",
            telefone="11987654321",
            placa="XYZ1234",
            usuario="joao123",
            senha="senha123",
            funcionario=self.funcionario
        )

        data = {
            "nome": "João Souza",
            "telefone": "11987654321",
            "placa": "XYZ1234",
            "usuario": "joao123",
            "senha": "nova_senha",
        }

        serializer = MotoboySerializerRequest(instance=motoboy, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

        updated_motoboy = serializer.save()
        self.assertEqual(updated_motoboy.nome, "João Souza")
        self.assertEqual(updated_motoboy.senha, "nova_senha")
        self.assertEqual(updated_motoboy.funcionario, self.funcionario)  # Funcionário não deve ser atualizado


class MotoboySerializerResponseTest(TestCase):
    
    def setUp(self):
        #Configura dados iniciais para os testes.

        #Cria um funcionário para ser usado nos testes
        self.funcionario = Funcionario.objects.create(
            nome="Victor Correa",
            cpf="697.023.938-17",
            email="victor.correa@gmail.com",
            usuario= "victorcorrea",
            senha="senha123"
        )

        # Cria um motoboy para ser usado nos testes
        self.motoboy = Motoboy.objects.create(
            nome="João Silva",
            telefone="11987654321",
            placa="XYZ1234",
            usuario="joao123",
            senha="senha123",
            funcionario=self.funcionario
        )

    def test_motoboy_serializer_response(self):
        #Testa se o MotoboySerializerResponse serializa os dados corretamente.
        serializer = MotoboySerializerResponse(instance=self.motoboy)
        expected_data = {
            "id": self.motoboy.id,
            "nome": "João Silva",
            "telefone": "11987654321",
            "placa": "XYZ1234",
            "funcionario": {
                "id": self.funcionario.id,
                "nome": "Victor Correa",
                "cpf": "697.023.938-17",
                "email": "victor.correa@gmail.com",
                "usuario": "victorcorrea",
                "senha": "senha123"
            },
            "usuario": "joao123",
            "senha": "senha123"
        }

        self.assertEqual(serializer.data, expected_data)

#Teste de urls.py

#Teste: se urls existem e retornam os status HTTP corretos, se cada url resolve a view correta, se a url gera o caminho esperado quando chamada por reverse()

class MotoboyURLsTest(TestCase):
   
    def setUp(self):
        #Configura dados iniciais para os testes.
        self.client = Client()

        # Cria um funcionário para ser usado nos testes
        self.funcionario = Funcionario.objects.create(
            nome="Victor Correa",
            cpf="697.023.938-17",
            email="victor.correa@gmail.com",
            usuario= "victorcorrea",
            senha="senha123"
        )

        # Cria um cliente para ser usado nos testes
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            telefone="11988888888",
            cep="13566710",
            logradouro="Rua Haiti",
            numero="123",
            complemento='B',
            bairro='Vila Brasília'
        )

        # Cria um produto para ser usado nos testes
        self.produto = Produto.objects.create(
            nome="Pizza Calabresa",
            preco=35.90
        )

        # Cria um motoboy para ser usado nos testes
        self.motoboy = Motoboy.objects.create(
            nome="João Silva",
            telefone="11987654321",
            placa="XYZ1234",
            usuario="joao123",
            senha="senha123",
            funcionario=self.funcionario
        )

    def test_motoboy_list_url(self):
        #Testa se a URL de listagem de motoboys está funcionando corretamente.
        url = reverse('motoboy-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_motoboy_add_url(self):
        #Testa se a URL de adição de motoboys está funcionando corretamente.
        url = reverse('motoboy-add')
 
        # Cria um funcionário antes de tentar criar um motoboy
        self.funcionario = Funcionario.objects.create(
            nome="Carlos Silva",
            cpf="91679717847",
            email = "carlos.silva@gmail.com",
            usuario = "carlos.silva",
            senha = "senha987"
        )

        #Usa POST para adicionar um motoboy
        response = self.client.post(url, data=json.dumps ({
            "nome": "Maria Souza",
            "telefone": "11987654321",
            "placa": "ABC1234",
            "usuario": "maria123",
            "senha": "senha123",
            "funcionario": self.funcionario.id
        }), content_type='application/json')
        print(response.status_code, response.content)
        self.assertEqual(response.status_code, 201)  # 201 Created

    def test_motoboy_detail_url(self):
        #Testa se a URL de detalhes de um motoboy está funcionando corretamente.
        url = reverse('motoboy-detail', args=[self.motoboy.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_motoboy_update_url(self):
        #Testa se a URL de atualização de um motoboy está funcionando corretamente.
        url = reverse('motoboy-update', args=[self.motoboy.pk])

        # Usa PUT para atualizar um motoboy
        response = self.client.put(url, data=json.dumps({
            "nome": "João Souza",
            "telefone": "11987654321",
            "placa": "XYZ1234",
            "usuario": "joao123",
            "senha": "nova_senha"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_motoboy_delete_url(self):
        #Testa se a URL de exclusão de um motoboy está funcionando corretamente.
        url = reverse('motoboy-delete', args=[self.motoboy.pk])

        # Usa DELETE para excluir um motoboy
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)  # 204 No Content

    def test_motoboy_login_url(self):
        #Testa se a URL de login de motoboys está funcionando corretamente.
        url = reverse('motoboy-login')
        
        # Usa POST para fazer login
        response = self.client.post(url, {
            "usuario": "joao123",
            "senha": "senha123"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
    def test_pedidos_motoboy_url(self):
        #Testa se a URL de pedidos de um motoboy está funcionando corretamente.
        #Cria um pedido associado ao motoboy
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            funcionario=self.funcionario,
            motoboy=self.motoboy,
            status="Em andamento",
            data_hora_inicio=timezone.now() #Adiciona o campo data_hora_inicio
        )
        pedido.produtos.add(self.produto)  # Adiciona o produto ao pedido

        url = reverse('pedidos-motoboy', args=[self.motoboy.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Verifica se o pedido foi retornado corretamente
        self.assertEqual(len(response.data), 1)  # Verifica se há 1 pedido na resposta
        self.assertEqual(response.data[0]['id'], pedido.id)  # Verifica se o ID do pedido está correto
        self.assertEqual(response.data[0]['status'], "Em andamento")  # Verifica o status do pedido

    def test_pedidos_motoboy_url_no_pedidos(self):
        #Testa se a URL de pedidos de um motoboy retorna 404 quando não há pedidos.
        url = reverse('pedidos-motoboy', args=[self.motoboy.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    #Teste de views.py

    #Teste: Testa os principais fluxos da API, incluindo criação, listagem, busca, atualização e remoção de motoboys, além da funcionalidade de login.

class MotoboyViewTests(TestCase):

    def setUp(self):
    # Configura dados iniciais para os testes.
        
        # Cria um funcionário
        self.funcionario = Funcionario.objects.create(
            nome="Carlos Oliveira",
            cpf="70541771850",
            email="carlos@example.com",
            usuario="carlos123",
            senha="senha123"
        )
     
        # Cria um motoboy
        self.motoboy_data = {
            "nome": "João Silva",
            "telefone": "11999999999",
            "placa": "ABC1234",
            "usuario": "joao123",
            "senha": "senha123",
            "funcionario" : self.funcionario.id #Enviar apenas o ID do funcionário
        }
        self.url = reverse('motoboy-add')

    def test_create_motoboy_success(self):
        # Criação de um motoboy com dados válidos
        response = self.client.post(self.url, self.motoboy_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Motoboy.objects.count(), 1)

    def test_create_motoboy_duplicate(self):
        # Primeiro cadastro
        response = self.client.post(self.url, self.motoboy_data, format='json', content_type ='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Segundo cadastro (mesmos nome/telefone/placa, mas usuario diferente)
        duplicate_data = {
            **self.motoboy_data,
            "usuario": "joao456"  # Altera o usuário para evitar conflito
        }
        response = self.client.post(self.url, duplicate_data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The fields nome, telefone, placa must make a unique set", str(response.data))

    def test_create_motoboy_invalid_data(self):
        # Tentativa de criação de um motoboy com dados inválidos
        invalid_data = {"nome": "", "telefone": "", "placa": "", "usuario": "", "senha": ""}
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class MotoboyListViewTests(TestCase):

    def setUp(self):
        # Configura dados iniciais para os testes.
        self.url = reverse('motoboy-list')
        Motoboy.objects.create(nome="João Silva", telefone="11999999999", placa="ABC1234", usuario="joao123", senha="senha123")

    def test_list_motoboys_success(self):
        # Listagem de todos os motoboys cadastrados
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_motoboys_empty(self):
        # Listagem de motoboys quando não há registros no banco
        Motoboy.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class MotoboyDetailViewTests(TestCase):

    def setUp(self):
        # Configura dados iniciais para os testes.        
        self.motoboy = Motoboy.objects.create(nome="João Silva", telefone="11999999999", placa="ABC1234", usuario="joao123", senha="senha123")
        self.url = reverse('motoboy-detail', args=[self.motoboy.id])

    def test_get_motoboy_success(self):
        # Recuperação de um motoboy existente
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], "João Silva")

    def test_get_motoboy_not_found(self):
        # Tentativa de recuperação de um motoboy inexistente
        invalid_url = reverse('motoboy-detail', args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MotoboyUpdateViewTests(TestCase):

    def setUp(self):
        # Configura dados iniciais para os testes.
        
        # Cria um funcionário
        self.funcionario = Funcionario.objects.create(
            nome="Carlos Oliveira",
            cpf="70541771850",
            email="carlos@example.com",
            usuario="carlos123",
            senha="senha123"
        )
        
        # Cria um motoboy inicial
        self.motoboy = Motoboy.objects.create(
            nome="João Silva",
            telefone="11999999999",
            placa="ABC1234",
            funcionario=self.funcionario,
            usuario="joao123",
            senha="senha123"
        )

        self.url = reverse('motoboy-update', args=[self.motoboy.id])

        # Atualiza o motoboy com novos dados 
        self.updated_data = {
            "nome": "João Souza", # Nome atualizado
            "telefone": "11888888888",  # Telefone atualizado
            "placa": "XYZ5678", # Placa atualizada
            "usuario": "joao123", # Mantém o mesmo usuário
            "senha": "senha123", # Mantém a mesma senha
            "funcionario": self.funcionario.id  # Adiciona o funcionário
        }

    def test_update_motoboy_success(self):
        # Atualização de um motoboy com dados válidos.
        response = self.client.put(self.url, data=json.dumps(self.updated_data),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.motoboy.refresh_from_db()
        self.assertEqual(self.motoboy.nome, "João Souza")

    def test_update_motoboy_duplicate(self):
        
        # Cria motoboy com placa duplicada
        outro_motoboy = Motoboy.objects.create(
            nome="Maria Silva",
            telefone="11777777777",
            placa="XYZ5678",  # Placa a duplicar
            funcionario=self.funcionario,
            usuario="maria123",
            senha="senha123"
    )
    
        # Tenta atualizar o segundo motoboy para ter os mesmos dados do primeiro
        duplicate_data = {
            "nome": self.motoboy.nome,
            "telefone": self.motoboy.telefone,
            "placa": self.motoboy.placa
        }
        
        response = self.client.put(
            reverse('motoboy-update', args=[outro_motoboy.id]),
            data=json.dumps(duplicate_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Response:", response.status_code, response.data)
        self.assertIn("The fields nome, telefone, placa must make a unique set", str(response.data))

class MotoboyDeleteViewTests(TestCase):

    def setUp(self):
        # Configura dados iniciais para os testes.
        self.motoboy = Motoboy.objects.create(nome="João Silva", telefone="11999999999", placa="ABC1234", usuario="joao123", senha="senha123")
        self.url = reverse('motoboy-delete', args=[self.motoboy.id])

    def test_delete_motoboy_success(self):
        # Exclusão de um motoboy existente.
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Motoboy.objects.count(), 0)

    def test_delete_motoboy_not_found(self):
        # Tentativa de exclusão de um motoboy inexistente.
        invalid_url = reverse('motoboy-delete', args=[999])
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MotoboyLoginViewTests(TestCase):

    def setUp(self):
        # Configura dados iniciais para os testes.
        self.motoboy = Motoboy.objects.create(nome="João Silva", telefone="11999999999", placa="ABC1234", usuario="joao123", senha="senha123")
        self.url = reverse('motoboy-login')

    def test_login_success(self):
        # Login de um motoboy com credenciais válidas.
        data = {"usuario": "joao123", "senha": "senha123"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], "João Silva")

    def test_login_invalid_credentials(self):
        # Tentativa de login com credenciais inválidas.
        data = {"usuario": "joao123", "senha": "senha_errada"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Credenciais inválidas", str(response.data))


class PedidosMotoboyViewTests(TestCase):
    
    def setUp(self):
        
        # Cria um funcionário
        self.funcionario = Funcionario.objects.create(
            nome="Carlos Oliveira",
            cpf="70541771850",
            email="carlos@example.com",
            usuario="carlos123",
            senha="senha123"
        )
        
        # Cria um motoboy
        self.motoboy = Motoboy.objects.create(
            nome="João Silva",
            telefone="11999999999",
            placa="ABC1234",
            funcionario=self.funcionario,
            usuario="joao123",
            senha="senha123"
        )

        # Cria um cliente
        self.cliente = Cliente.objects.create(
            nome="Maria Souza",
            telefone="11987654321",
            cep="13575140",
            logradouro="Rua João Ribeiro de Souza Filho",
            numero="123",
            bairro="Jardim Beatriz"
        )

        # Cria um produto
        self.produto = Produto.objects.create(
            nome="Pizza calabresa",
            preco=10.50
        )

        # Cria um pedido associado ao motoboy
        self.pedido = Pedido.objects.create(
            data_hora_inicio=timezone.now(),
            cliente=self.cliente,
            funcionario=self.funcionario,
            motoboy=self.motoboy,
            status="em_andamento"
        )
        self.pedido.produtos.add(self.produto)  # Adiciona o produto ao pedido

        self.url = reverse('pedidos-motoboy', args=[self.motoboy.id])


    def test_get_pedidos_success(self):
        # Listagem de pedidos associados a um motoboy.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Verifica se há 1 pedido na resposta

    def test_get_pedidos_empty(self):
        # Listagem de pedidos associados a um motoboy sem pedidos
        Pedido.objects.all().delete() # Remove todos os pedidos associados ao motoboy
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Nenhum pedido encontrado", str(response.data))