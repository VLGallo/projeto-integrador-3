from django.db import models


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15)
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=30, null=True, blank=True)
    bairro = models.CharField(max_length=200)

# garante que se todos os campos forem iguais simultaneamente, não permite o cadastro duas vezes do mesmo cliente com id diferente
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['nome', 'telefone', 'cep', 'logradouro', 'numero', 'complemento', 'bairro'],
                name='unique_cliente'
            )
        ]

    def __str__(self):
        return self.nome
