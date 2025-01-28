from rest_framework.exceptions import NotFound, ValidationError
from django.db import IntegrityError
from .models import Motoboy
from .serializers import MotoboySerializerResponse, MotoboySerializerRequest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class MotoboyView(APIView):
    def post(self, request):
        serializer = MotoboySerializerRequest(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            motoboy = serializer.save()

            response_data = MotoboySerializerResponse(motoboy).data
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            raise ValidationError({"detail": "Motoboy já cadastrado com o mesmo nome, telefone e placa."})


class MotoboyListView(APIView):
    def get(self, request):
        companies = Motoboy.objects.all().order_by('id')
        serializer = MotoboySerializerResponse(companies, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class MotoboyDetailView(APIView):
    def get_object(self, pk):
        try:
            return Motoboy.objects.get(pk=pk)
        except Motoboy.DoesNotExist:
            raise NotFound("Motoboy não encontrado")

    def get(self, request, pk):
        motoboy = self.get_object(pk)
        serializer = MotoboySerializerResponse(motoboy)
        return Response(serializer.data)


class MotoboyUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Motoboy.objects.get(pk=pk)
        except Motoboy.DoesNotExist:
            raise NotFound("Motoboy não encontrado")

    def put(self, request, pk):
        motoboy = self.get_object(pk)
        serializer = MotoboySerializerRequest(motoboy, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except IntegrityError:
            raise ValidationError({"detail": "Outro motoboy já cadastrado com o mesmo nome, telefone e placa."})


class MotoboyDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Motoboy.objects.get(pk=pk)
        except Motoboy.DoesNotExist:
            raise NotFound("Motoboy não encontrado")

    def delete(self, request, pk):
        motoboy = self.get_object(pk)
        motoboy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data="Motoboy deletado com sucesso")