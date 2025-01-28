from django.db import models


class Funcionario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    usuario = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
