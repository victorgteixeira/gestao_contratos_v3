# Generated by Django 5.1.2 on 2024-11-11 12:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0037_alter_contrato_observacao_rateio_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='mention_users',
            field=models.ManyToManyField(blank=True, related_name='mentioned_contratos', to=settings.AUTH_USER_MODEL),
        ),
    ]