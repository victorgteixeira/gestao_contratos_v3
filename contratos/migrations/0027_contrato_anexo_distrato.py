# Generated by Django 5.1.2 on 2024-10-31 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0026_contrato_flag_distrato_contrato_flag_rateio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='anexo_distrato',
            field=models.FileField(blank=True, null=True, upload_to='distrato/'),
        ),
    ]
