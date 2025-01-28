from datetime import datetime
from django.db import models
from gerenciador_de_clientes.models import Cliente
from gerenciador_de_funcionarios.models import Funcionario
from gerenciador_de_produtos.models import Produto
from gerenciador_de_motoboys.models import Motoboy

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('em_andamento', 'Em andamento'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    data_hora_inicio = models.DateTimeField()
    data_hora_finalizacao = models.DateTimeField(null=True, blank=True)
    produtos = models.ManyToManyField(Produto)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='pedidos', null=True, blank=True)
    motoboy = models.ForeignKey(Motoboy, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_andamento')

    def save(self, *args, **kwargs):
        if not self.pk and self.status == 'em_andamento':
            self.data_hora_inicio = self.data_hora_inicio or datetime.now()
        if self.status == 'entregue' or self.status == 'cancelado':
            self.data_hora_finalizacao = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido iniciado em {self.data_hora_inicio} para {self.cliente}"
