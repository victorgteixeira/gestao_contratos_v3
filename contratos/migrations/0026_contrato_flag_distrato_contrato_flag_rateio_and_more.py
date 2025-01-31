# Generated by Django 5.1.2 on 2024-10-31 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0025_alter_contrato_area_beneficiada_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='flag_distrato',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contrato',
            name='flag_rateio',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contrato',
            name='observacao_distrato',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
    ]
