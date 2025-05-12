from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


def validate_max_digits(value):
    # Remove o ponto decimal e verifica o comprimento
    if len(str(value).replace('.', '')) > 10:
        raise ValidationError('Certifique-se de que não tenha mais de 10 dígitos no total.')

class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'), validate_max_digits)])
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nome', 'preco'], name='unique_produto_nome_preco')
        ]
    def __str__(self):
        return self.nome