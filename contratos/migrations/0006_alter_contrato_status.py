# Generated by Django 5.1.2 on 2024-10-18 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0005_contrato_data_criacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='status',
            field=models.CharField(blank=True, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], max_length=10, null=True),
        ),
    ]
