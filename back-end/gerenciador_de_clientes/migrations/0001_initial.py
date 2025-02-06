# Generated by Django 5.0.3 on 2025-02-06 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('telefone', models.CharField(max_length=15)),
                ('cep', models.CharField(max_length=8)),
                ('logradouro', models.CharField(max_length=200)),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=30, null=True)),
                ('bairro', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddConstraint(
            model_name='cliente',
            constraint=models.UniqueConstraint(fields=('nome', 'telefone', 'cep', 'logradouro', 'numero', 'complemento', 'bairro'), name='unique_cliente'),
        ),
    ]
