# Generated by Django 5.1.2 on 2024-11-06 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0035_historicocontrato_campos_alterados'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='c_contabil',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
