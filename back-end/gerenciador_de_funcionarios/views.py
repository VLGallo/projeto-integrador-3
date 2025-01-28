from rest_framework.exceptions import NotFound, ValidationError
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import Funcionario
from .serializers import FuncionarioSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class FuncionarioView(APIView):
    def post(self, request):
        serializer = FuncionarioSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            response_data = FuncionarioSerializer(user).data
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            # Tratamento para campos únicos: CPF, Email e Usuário
            if 'cpf' in str(e):
                raise ValidationError({"detail": "CPF já cadastrado."})
            elif 'email' in str(e):
                raise ValidationError({"detail": "Email já cadastrado."})
            elif 'usuario' in str(e):
                raise ValidationError({"detail": "Usuário já cadastrado."})
            else:
                raise ValidationError({"detail": "Erro ao cadastrar o funcionário."})

class FuncionarioListView(APIView):
    def get(self, request):
        funcionarios = Funcionario.objects.all().order_by('id')
        serializer = FuncionarioSerializer(funcionarios, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FuncionarioDetailView(APIView):
    def get_object(self, pk):
        try:
            return Funcionario.objects.get(pk=pk)
        except Funcionario.DoesNotExist:
            raise NotFound("Funcionário não encontrado")

    def get(self, request, pk):
        funcionario = self.get_object(pk)
        serializer = FuncionarioSerializer(funcionario)
        return Response(serializer.data)

from rest_framework.exceptions import ValidationError
from django.db import IntegrityError


class FuncionarioUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Funcionario.objects.get(pk=pk)
        except Funcionario.DoesNotExist:
            raise NotFound("Funcionário não encontrado")

    def put(self, request, pk):
        funcionario = self.get_object(pk)
        serializer = FuncionarioSerializer(funcionario, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except IntegrityError as e:
            raise ValidationError({"detail": "Erro ao atualizar o funcionário."})


class FuncionarioDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Funcionario.objects.get(pk=pk)
        except Funcionario.DoesNotExist:
            raise NotFound("Funcionário não encontrado")

    def delete(self, request, pk):
        funcionario = self.get_object(pk)
        funcionario.delete()
        return Response(status=status.HTTP_202_ACCEPTED, data="Funcionário deletado com sucesso")


class FuncionarioLoginView(APIView):
    def post(self, request):
        usuario = request.data.get('usuario')
        senha = request.data.get('senha')
        funcionario = get_object_or_404(Funcionario, usuario=usuario)
        if funcionario is not None and funcionario.usuario == usuario and funcionario.senha == senha:
            return Response(data={"message": "Login bem-sucedido"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED)