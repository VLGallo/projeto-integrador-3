from django.db import models
from gerenciador_de_funcionarios.models import Funcionario


class Motoboy(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=30)
    placa = models.CharField(max_length=20)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nome', 'telefone', 'placa'],
                name='unique_motoboy'
            )
        ]

    def __str__(self):
        return self.nome