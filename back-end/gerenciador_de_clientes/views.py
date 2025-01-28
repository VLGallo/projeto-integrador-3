from rest_framework.exceptions import ValidationError, NotFound
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteView(APIView):
    def post(self, request):
        # Obter os dados do corpo da requisição
        nome = request.data.get('nome')
        telefone = request.data.get('telefone')
        cep = request.data.get('cep').replace('-', '').strip()
        logradouro = request.data.get('logradouro')
        numero = request.data.get('numero')
        bairro = request.data.get('bairro')

        # Validação de todos os campos obrigatórios
        if not nome or not telefone or not cep or not logradouro or not numero or not bairro:
            return Response({"error": "Preencher todos os campos obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        # Preparar dados para o serializer
        serializer = ClienteSerializer(data={
            'nome': nome,
            'telefone': telefone,
            'cep': cep,
            'logradouro': logradouro,
            'numero': numero,
            'complemento': request.data.get('complemento', ''),
            'bairro': bairro
        })

        try:
            serializer.is_valid(raise_exception=True)
            cliente = serializer.save()
            response_data = ClienteSerializer(cliente).data
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            raise ValidationError({"detail": "Cliente já cadastrado com os mesmos dados."})

class ClienteListView(APIView):
    def get(self, request):
        clientes = Cliente.objects.all().order_by('nome')
        serializer = ClienteSerializer(clientes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ClienteDetailView(APIView):
    def get_object(self, pk):
        try:
            return Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            raise NotFound("Cliente não encontrado")

    def get(self, request, pk):
        cliente = self.get_object(pk)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

class ClienteUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            raise NotFound("Cliente não encontrado.")

    def put(self, request, pk):
        cliente = self.get_object(pk)

        nome = request.data.get('nome', cliente.nome)
        telefone = request.data.get('telefone', cliente.telefone)
        cep = request.data.get('cep', cliente.cep).replace('-', '').strip()
        logradouro = request.data.get('logradouro', cliente.logradouro)
        bairro = request.data.get('bairro', cliente.bairro)
        numero = request.data.get('numero', cliente.numero)

        # Verificar se todos os campos obrigatórios estão presentes
        if not nome or not cep or not logradouro or not bairro or not telefone or not numero:
            return Response({"error": "Nome, CEP, logradouro, bairro, telefone e número são obrigatórios."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Preparar os dados para o serializer
        serializer = ClienteSerializer(cliente, data={
            'nome': nome,
            'telefone': telefone,
            'cep': cep,
            'logradouro': logradouro,
            'numero': numero,
            'complemento': request.data.get('complemento', cliente.complemento),
            'bairro': bairro
        })

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except IntegrityError:
            raise ValidationError({"detail": "Outro cliente já cadastrado com os mesmos dados."})

class ClienteDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            raise NotFound("Cliente não encontrado")

    def delete(self, request, pk):
        cliente = self.get_object(pk)
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data="Cliente deletado com sucesso")

class BuscaCepView(APIView):
    def get(self, request, cep):
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if response.status_code != 200 or 'erro' in response.json():
            return Response({"error": "CEP inválido."}, status=status.HTTP_400_BAD_REQUEST)

        endereco_data = response.json()
        logradouro = endereco_data.get('logradouro', '')
        bairro = endereco_data.get('bairro', '')

        return Response({"logradouro": logradouro, "bairro": bairro}, status=status.HTTP_200_OK)
