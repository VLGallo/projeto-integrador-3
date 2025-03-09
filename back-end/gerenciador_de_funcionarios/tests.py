from django.test import TestCase
from gerenciador_de_funcionarios.models import Funcionario
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from gerenciador_de_funcionarios.serializers import FuncionarioSerializer
from django.urls import reverse, resolve
from gerenciador_de_funcionarios.views import (
    FuncionarioView,
    FuncionarioListView,
    FuncionarioDetailView,
    FuncionarioUpdateView,
    FuncionarioDeleteView,
    FuncionarioLoginView,
)
from rest_framework.test import APIClient
from rest_framework import status

#Teste de models.py

#Teste: criar um funcionário válido, testar o tamanho dos campos, testar se os campos CPF, e-mail e usuário são únicos, testar o preenchimento de campos obrigatórios e a conversão para sting (_str_)

class FuncionarioModelTest(TestCase):

    def setUp(self):
        #Configura um funcionário antes de cada teste
        self.funcionario = Funcionario.objects.create(
            nome="Fábio Duarte",
            cpf="545.117.628-05",
            email="fabio.duarte@gmail.com",
            usuario="fabioduarte",
            senha="senha123"
        )

    def test_criacao_funcionario(self):
        #Testa a criação de um funcionário e verifica se o campos foram criados corretamente
        self.assertEqual(self.funcionario.nome, "Fábio Duarte")
        self.assertEqual(self.funcionario.cpf, "545.117.628-05")
        self.assertEqual(self.funcionario.email, "fabio.duarte@gmail.com")
        self.assertEqual(self.funcionario.usuario, "fabioduarte")
        self.assertEqual(self.funcionario.senha, "senha123")

    def test_cpf_unico(self):
        #Testa se o CPF é único tentando criar um segundo funcionário com o mesmo CPF
        with self.assertRaises(Exception):
            Funcionario.objects.create(
                nome="Maria Oliveira",
                cpf="545.117.628-05",  # CPF duplicado
                email="maria.oliveira@gmail.com",
                usuario="mariaoliveira",
                senha="senha456"
            )

    def test_email_unico(self):
        #Testa se o email é único tentando criar um segundo funcionário com o mesmo email
        with self.assertRaises(Exception):
            Funcionario.objects.create(
                nome="Carlos Souza",
                cpf="947.672.568-01",
                email="fabio.duarte@gmail.com",  # Email duplicado
                usuario="carlossouza",
                senha="senha789"
            )

    def test_usuario_unico(self):
        #Testa se o usuário é único tentando criar um segundo funcionário com o mesmo usuário
        with self.assertRaises(Exception):
            Funcionario.objects.create(
                nome="Ana Costa",
                cpf="124.056.348-56",
                email="ana.costa@gmail.com",
                usuario="fabioduarte",  # Usuário duplicado
                senha="senha101"
            )

    def test_str_representation(self):
        #Testa a representação em string do modelo
        self.assertEqual(str(self.funcionario), "Fábio Duarte")
 
    def test_required_fields(self):
        #Testa se os campos obrigatórios estão realmente sendo validados
        #Dados válidos para o funcionário
        data = {
            "nome": "Fábio Duarte",
            "cpf": "545.117.628-05",
            "email": "fabio.duarte@gmail.com",
            "usuario": "fabioduarte",
            "senha": "senha123"
        }
        #Lista de campos obrigatórios
        required_fields = ["nome", "cpf", "email", "usuario", "senha"]

        for field in required_fields:
            #Cria uma cópia dos dados válidos
            test_data = data.copy()

            #Remove o campo a ser testado
            test_data.pop(field)  

            #Cria o serializer com os dados incompletos
            serializer = FuncionarioSerializer(data=test_data)

            #Verifica se o serializer é inválido
            self.assertFalse(serializer.is_valid())

            #Verifica se o campo removido está na lista de erros
            self.assertIn(field, serializer.errors)

class FuncionarioFieldSizeTests(TestCase):

    def test_valid_max_lengths(self):
        #Testa se os valores no limite máximo são aceitos.
        # Dados válidos para o funcionário
        valid_data = {
            "nome": "Fábio Duarte",
            "cpf": "545.117.628-05",
            "email": "fabio.duarte@gmail.com",
            "usuario": "fabioduarte",
            "senha": "senha123"
        }

        # Limites máximos de tamanho para cada campo
        max_lengths = {
            "nome": 200,
            "cpf": 14,  # CPF com pontos e traço
            "email": 254,
            "usuario": 100,
            "senha": 100,
        }

        for field, max_length in max_lengths.items():
            # Cria uma cópia dos dados válidos
            data = valid_data.copy()
        
        # Define o valor do campo no limite máximo
        if field == "cpf":
            # CPF no formato XXX.XXX.XXX-XX (14 caracteres)
            data[field] = "123.456.789-09"
        else:
            data[field] = "A" * max_length  # Preenche o campo com "A" até o limite máximo
        
        # Cria o serializer com os dados
        serializer = FuncionarioSerializer(data=data)
        
        # Verifica se o serializer é válido
        self.assertTrue(serializer.is_valid(), f"Campo {field} falhou: {serializer.errors}")

#Teste de serializers.py

#Teste: Validação de CPF (CPF válido, CPF com menos de 11 dígitos, CPF com todos os dígitos iguais, CPF com dígitos verificadores inválidos, CPF já existente na base), validação de e-mail (e-mail válido, e-mail com formato inválido, e-mail já existente na base), validação de usuário (usuário válido, usuário já existente na base), serialização e desserialização.

class FuncionarioSerializerTest(TestCase):

    def setUp(self):
        # Cria um funcionário para testes de unicidade
        self.funcionario_existente = Funcionario.objects.create(
            nome="João Silva",
            cpf="867.124.868-23",
            email="joao.silva@gmail.com",
            usuario="joaosilva",
            senha="senha123"
        )

    # Testes de Validação de CPF
    def test_cpf_valido(self):
        #Testa um CPF válido
        data = {
            "nome": "Maria Oliveira",
            "cpf": "872.652.048-67",
            "email": "maria.oliveira@gmail.com",
            "usuario": "mariaoliveira",
            "senha": "senha456"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_cpf_limpo(self):
        #Testa se o CPF é limpo corretamente, removendo pontos e traço.
        # Dados válidos para o funcionário
        data = {
            "nome": "Fábio Duarte",
            "cpf": "545.117.628-05",  # CPF com pontos e traço
            "email": "fabio.duarte@gmail.com",
            "usuario": "fabioduarte",
            "senha": "senha123"
        }

        # Cria o serializer com os dados
        serializer = FuncionarioSerializer(data=data)
    
        # Verifica se o serializer é válido
        self.assertTrue(serializer.is_valid(), serializer.errors)
    
        # Verifica se o CPF foi limpo corretamente
        self.assertEqual(serializer.validated_data["cpf"], "54511762805")  # CPF sem pontos e traço

    def test_cpf_com_menos_de_11_digitos(self):
        #Testa um CPF com menos de 11 dígitos.
        data = {
            "nome": "Carlos Souza",
            "cpf": "123.456",
            "email": "carlos.souza@gmail.com",
            "usuario": "carlossouza",
            "senha": "senha789"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("CPF deve conter 11 dígitos.", serializer.errors["cpf"])

    def test_cpf_com_digitos_iguais(self):
        #Testa um CPF com todos os dígitos iguais.
        data = {
            "nome": "Ana Costa",
            "cpf": "111.111.111-11",
            "email": "ana.costa@gmail.com",
            "usuario": "anacosta",
            "senha": "senha101"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("CPF inválido.", serializer.errors["cpf"])

    def test_cpf_com_digitos_verificadores_invalidos(self):
        #Testa um CPF com dígitos verificadores inválidos.
        data = {
            "nome": "Pedro Alves",
            "cpf": "123.456.789-00",
            "email": "pedro.alves@gmail.com",
            "usuario": "pedroalves",
            "senha": "senha202"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cpf", serializer.errors)

    def test_cpf_ja_existente(self):
        #Testa um CPF já existente na base.
        data = {
            "nome": "João Silva",
            "cpf": "867.124.868-23",  # CPF já existente (mesmo do SetUp)
            "email": "joao.silva2@gmail.com",
            "usuario": "joaosilva2",
            "senha": "senha123"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("funcionario com este cpf já existe.", serializer.errors["cpf"])

    # Testes de Validação de Email
    def test_email_valido(self):
        #Testa um email válido.
        data = {
            "nome": "Fernanda Lima",
            "cpf": "305.326.708-09",
            "email": "fernanda.lima@gmail.com",
            "usuario": "fernandalima",
            "senha": "senha303"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_email_formato_invalido(self):
        #Testa um email com formato inválido.
        data = {
            "nome": "Ricardo Almeida",
            "cpf": "164.629.008-90",
            "email": "ricardo.almeida",  # Email inválido
            "usuario": "ricardoalmeida",
            "senha": "senha404"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Informe um endereço de email válido.", serializer.errors["email"])

    def test_email_ja_existente(self):
        #Testa um email já existente na base.
        data = {
            "nome": "João Silva",
            "cpf": "774.685.248-31",
            "email": "joao.silva@gmail.com",  # Email já existente (mesmo do setUp)
            "usuario": "joaosilva3",
            "senha": "senha123"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("funcionario com este email já existe.", serializer.errors["email"])

    # Testes de Validação de Usuário
    def test_usuario_valido(self):
        #Testa um usuário válido.
        data = {
            "nome": "Luciana Santos",
            "cpf": "518.523.608-60",
            "email": "luciana.santos@gmail.com",
            "usuario": "lucianasantos",
            "senha": "senha505"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_usuario_ja_existente(self):
        #Testa um usuário já existente na base.
        data = {
            "nome": "João Silva",
            "cpf": "774.685.248-31",
            "email": "joao.silva3@gmail.com",
            "usuario": "joaosilva",  # Usuário já existente
            "senha": "senha123"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("funcionario com este usuario já existe.", serializer.errors["usuario"])

    # Testes de Serialização e Desserialização
    def test_serializacao(self):
        #Testa a serialização de um objeto Funcionario.
        funcionario = Funcionario.objects.create(
            nome="Carlos Eduardo",
            cpf="564.412.088-06",
            email="carlos.eduardo@gmail.com",
            usuario="carloseduardo",
            senha="senha606"
        )
        serializer = FuncionarioSerializer(funcionario)
        expected_data = {
            "id": funcionario.id,
            "nome": "Carlos Eduardo",
            "cpf": "564.412.088-06",
            "email": "carlos.eduardo@gmail.com",
            "usuario": "carloseduardo",
            "senha": "senha606"
        }
        self.assertEqual(serializer.data, expected_data)

    def test_desserializacao(self):
        #Testa a desserialização de dados válidos.
        data = {
            "nome": "Ana Paula",
            "cpf": "962.159.478-22",
            "email": "ana.paula@gmail.com",
            "usuario": "anapaula",
            "senha": "senha707"
        }
        serializer = FuncionarioSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        funcionario = serializer.save()
        self.assertEqual(funcionario.nome, "Ana Paula")
        self.assertEqual(funcionario.cpf, "96215947822")
        self.assertEqual(funcionario.email, "ana.paula@gmail.com")
        self.assertEqual(funcionario.usuario, "anapaula")
        self.assertEqual(funcionario.senha, "senha707")

#Teste de urls.py

#Testes: se urls existem e retornam os status HTTP corretos, se cada url resolve a view correta, se a url gera o caminho esperado quando chamada por reverse()

class UrlsTest(TestCase):

    # Testes de resolução (resolve()): verificam se a url definida no urlpatterns realmente chama a view correta.

    def test_funcionario_list_url_resolves(self):
        # Testa se a URL '/funcionario' resolve para FuncionarioListView
        url = '/funcionario'
        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__, FuncionarioListView.as_view().__name__)

    def test_funcionario_add_url_resolves(self):
        # Testa se a URL '/funcionario/add' resolve para FuncionarioView
        url = '/funcionario/add'
        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__, FuncionarioView.as_view().__name__)

    def test_funcionario_detail_url_resolves(self):
        # Testa se a URL '/funcionario/<int:pk>' resolve para FuncionarioDetailView
        url = '/funcionario/1'  # Sendo '1' exemplo de ID
        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__, FuncionarioDetailView.as_view().__name__)

    def test_funcionario_update_url_resolves(self):
        # Testa se a URL '/funcionario/update/<int:pk>' resolve para FuncionarioUpdateView
        url = '/funcionario/update/1'  # Sendo '1' exemplo de ID
        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__, FuncionarioUpdateView.as_view().__name__)

    def test_funcionario_delete_url_resolves(self):
        # Testa se a URL '/funcionario/delete/<int:pk>' resolve para FuncionarioDeleteView
        url = '/funcionario/delete/1'  # Sendo '1' exemplo de ID
        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__, FuncionarioDeleteView.as_view().__name__)

    def test_login_url_resolves(self):
        # Testa se a URL '/login' resolve para FuncionarioLoginView
        url = '/login'
        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__, FuncionarioLoginView.as_view().__name__)


    # Testes de reverse(): Garantem que os nomes das urls retornam os caminhos corretos quando utilizados em templates ou chamadas de API.

    def test_funcionario_list_url_reverse(self):
        # Testa a URL '/funcionario' usando reverse
        url = reverse('funcionario-list')  
        self.assertEqual(url, '/funcionario')

    def test_funcionario_add_url_reverse(self):
        # Testa a URL '/funcionario/add' usando reverse
        url = reverse('funcionario-add')  
        self.assertEqual(url, '/funcionario/add')

    def test_funcionario_detail_url_reverse(self):
        # Testa a URL '/funcionario/<int:pk>' usando reverse
        url = reverse('funcionario-detail', args=[1])  # Passa o ID como argumento
        self.assertEqual(url, '/funcionario/1')

    def test_funcionario_update_url_reverse(self):
        # Testa a URL '/funcionario/update/<int:pk>' usando reverse
        url = reverse('funcionario-update', args=[1])  # Passa o ID como argumento
        self.assertEqual(url, '/funcionario/update/1')

    def test_funcionario_delete_url_reverse(self):
        # Testa a URL '/funcionario/delete/<int:pk>' usando reverse
        url = reverse('funcionario-delete', args=[1])  # Passa o ID como argumento
        self.assertEqual(url, '/funcionario/delete/1')

    def test_login_url_reverse(self):
        # Testa a URL '/login' usando reverse
        url = reverse('login')  
        self.assertEqual(url, '/login')

#Teste de views.py

#Teste: Testa os principais fluxos da API, incluindo criação, listagem, busca, atualização e remoção de funcionários, além da funcionalidade de login.

class FuncionarioViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.funcionario_data = {
            "nome": "Fábio Duarte",
            "cpf": "545.117.628-05",
            "email": "fabio.duarte@gmail.com",
            "usuario": "fabioduarte",
            "senha": "senha123"
        }
        self.url = reverse('funcionario-add')

    def test_criar_funcionario_valido(self):
        # Testa a criação de um funcionário com dados válidos
        response = self.client.post(self.url, self.funcionario_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Funcionario.objects.count(), 1)
        self.assertEqual(Funcionario.objects.get().nome, "Fábio Duarte")

    def test_criar_funcionario_cpf_existente(self):
        # Testa a criação de um funcionário com CPF já existente
        Funcionario.objects.create(**self.funcionario_data)
        response = self.client.post(self.url, self.funcionario_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("funcionario com este cpf já existe.", str(response.data))

    def test_criar_funcionario_email_existente(self):
        # Testa a criação de um funcionário com email já existente
        Funcionario.objects.create(**self.funcionario_data)

        novo_funcionario_data = self.funcionario_data.copy()
        novo_funcionario_data["cpf"] = "987.654.321-09"  # Altera o CPF
        novo_funcionario_data["usuario"] = "novousuario"  # Altera o usuário

        response = self.client.post(self.url, novo_funcionario_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("funcionario com este email já existe.", str(response.data))

    def test_criar_funcionario_usuario_existente(self):
        # Testa a criação de um funcionário com usuário já existente
        Funcionario.objects.create(**self.funcionario_data)
        
        novo_funcionario_data = self.funcionario_data.copy()
        novo_funcionario_data["cpf"] = "987.654.321-09"  # Altera o CPF
        novo_funcionario_data["email"] = "novoemail@gmail.com"  # Altera o email
        
        response = self.client.post(self.url, novo_funcionario_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("funcionario com este usuario já existe.", str(response.data))
    
    def test_criar_funcionario_dados_invalidos(self):
        # Testa a criação de um funcionário com dados inválidos
        invalid_data = self.funcionario_data.copy()
        invalid_data["cpf"] = "123"  # CPF inválido
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class FuncionarioListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('funcionario-list')
        Funcionario.objects.create(
            nome="João Silva",
            cpf="123.456.789-09",
            email="joao.silva@gmail.com",
            usuario="joaosilva",
            senha="senha123"
        )

    def test_listar_funcionarios(self):
        # Testa a listagem de todos os funcionários
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["nome"], "João Silva")


class FuncionarioDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.funcionario = Funcionario.objects.create(
            nome="Maria Oliveira",
            cpf="987.654.321-00",
            email="maria.oliveira@gmail.com",
            usuario="mariaoliveira",
            senha="senha456"
        )
        self.url = reverse('funcionario-detail', args=[self.funcionario.id])

    def test_recuperar_funcionario_existente(self):
        # Testa a recuperação de um funcionário existente
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], "Maria Oliveira")

    def test_recuperar_funcionario_inexistente(self):
        # Testa a tentativa de recuperar um funcionário inexistente
        invalid_url = reverse('funcionario-detail', args=[999])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FuncionarioUpdateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.funcionario = Funcionario.objects.create(
            nome="Carlos Souza",
            cpf="021.233.208-20",
            email="carlos.souza@gmail.com",
            usuario="carlossouza",
            senha="senha789"
        )
        self.url = reverse('funcionario-update', args=[self.funcionario.id])

    def test_atualizar_funcionario_valido(self):
        # Testa a atualização de um funcionário com dados válidos
        updated_data = {
            "nome": "Carlos Eduardo",
            "cpf": "021.233.208-20",  # Mantém o CPF original
            "email": "carlos.souza@gmail.com",  # Mantém o email original
            "usuario": "carlossouza",  # Mantém o usuário original
            "senha": "senha789"  # Mantém a senha original
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.funcionario.refresh_from_db()
        self.assertEqual(self.funcionario.nome, "Carlos Eduardo")

    def test_atualizar_funcionario_inexistente(self):
        # Testa a tentativa de atualizar um funcionário inexistente
        invalid_url = reverse('funcionario-update', args=[999])
        response = self.client.put(invalid_url, {"nome": "Carlos Eduardo"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_atualizar_funcionario_dados_invalidos(self):
        # Testa a atualização de um funcionário com dados inválidos
        invalid_data = {"cpf": "123"}  # CPF inválido
        response = self.client.put(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FuncionarioDeleteViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.funcionario = Funcionario.objects.create(
            nome="Ana Costa",
            cpf="062.924.228-36",
            email="ana.costa@gmail.com",
            usuario="anacosta",
            senha="senha101"
        )
        self.url = reverse('funcionario-delete', args=[self.funcionario.id])

    def test_excluir_funcionario_existente(self):
        # Testa a exclusão de um funcionário existente
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Funcionario.objects.count(), 0)

    def test_excluir_funcionario_inexistente(self):
        # Testa a tentativa de excluir um funcionário inexistente
        invalid_url = reverse('funcionario-delete', args=[999])
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FuncionarioLoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.funcionario = Funcionario.objects.create(
            nome="Pedro Alves",
            cpf="884.268.848-73",
            email="pedro.alves@gmail.com",
            usuario="pedroalves",
            senha="senha202"
        )
        self.url = reverse('login')

    def test_login_credenciais_validas(self):
        # Testa o login com credenciais válidas
        data = {"usuario": "pedroalves", "senha": "senha202"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login bem-sucedido")

    def test_login_credenciais_invalidas(self):
        # Testa o login com credenciais inválidas
        data = {"usuario": "pedroalves", "senha": "senhaerrada"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["message"], "Credenciais inválidas")