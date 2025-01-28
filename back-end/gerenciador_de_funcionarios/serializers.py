from rest_framework import serializers
from .models import Funcionario
import re

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ['id', 'nome', 'cpf', 'email', 'usuario', 'senha']

    # Validação de CPF
    def validate_cpf(self, value):
        cpf = re.sub(r'\D', '', value)  # Remove pontos e traços

        # Verificar se o CPF tem 11 dígitos
        if len(cpf) != 11:
            raise serializers.ValidationError("CPF deve conter 11 dígitos.")

        # Verificar se todos os dígitos são iguais, o que é inválido para CPF
        if cpf == cpf[0] * 11:
            raise serializers.ValidationError("CPF inválido.")

        # Função para calcular o dígito verificador
        def calcular_digito(digitos):
            soma = sum((len(digitos) + 1 - i) * int(d) for i, d in enumerate(digitos))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        # Verificar os dois dígitos verificadores
        if cpf[9] != calcular_digito(cpf[:9]) or cpf[10] != calcular_digito(cpf[:10]):
            raise serializers.ValidationError("CPF inválido.")

        # Verificar se o CPF já está em uso por outro funcionário
        funcionario_id = self.instance.id if self.instance else None
        if Funcionario.objects.filter(cpf=value).exclude(id=funcionario_id).exists():
            raise serializers.ValidationError("CPF já existente na base.")

        return value

    # Validação de Email
    def validate_email(self, value):
        email = value.lower()  # Padroniza o email para minúsculas
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise serializers.ValidationError("Formato de email inválido.")

        # Verificar se o email já está em uso por outro funcionário
        funcionario_id = self.instance.id if self.instance else None
        if Funcionario.objects.filter(email=email).exclude(id=funcionario_id).exists():
            raise serializers.ValidationError("Email já existente na base.")

        return email

    # Validação de Usuário
    def validate_usuario(self, value):
        # Verificar se o usuário já está em uso por outro funcionário
        funcionario_id = self.instance.id if self.instance else None
        if Funcionario.objects.filter(usuario=value).exclude(id=funcionario_id).exists():
            raise serializers.ValidationError("Usuário já existente na base.")

        return value
