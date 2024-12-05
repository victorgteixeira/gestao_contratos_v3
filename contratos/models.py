import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from cnpj_field.models import CNPJField
from cpf_field.models import CPFField
from django.core.validators import RegexValidator

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    c_contabil = models.CharField(max_length=100, unique=False, null=True, blank=True)

    def __str__(self):
        return self.nome

class PastaBiblioteca(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    
class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = CNPJField(max_length=15)
    cpf = CPFField('cpf')
    #email = models.EmailField(unique=True)
    #telefone = models.CharField(
    #    max_length=20,
    #    validators=[RegexValidator(r'^\d+$', 'Apenas números são permitidos no campo de telefone.')]
    #)
    endereco = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome

class Contrato(models.Model):

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('encerrado', 'Encerrado'),
    ]
    
    IMOBILIZADO_DESPESA_CHOICES = [
        ('imobilizado', 'Imobilizado'),
        ('despesa', 'Despesa'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('fixo', 'Fixo'),
        ('variavel', 'Variável'),
        ('outros', 'Outros'),
    ]
    
    INDICE_REAJUSTE_CHOICES = [
        ('igpm', 'IGPM'),
        ('ipca', 'IPCA'),
        ('inpc', 'INPC'),
        ('outros', 'Outros'),
    ]

    # Contratos
    referencia_contrato = models.CharField(max_length=5, unique=True, blank=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)
    responsavel = models.CharField(max_length=255, null=True, blank=True)
    contrato_file = models.FileField(upload_to='contratos/', null=True, blank=True) 
    imagem = models.ImageField(upload_to='imagens/', null=True, blank=True) 
    observacao_contrato = models.TextField(max_length=500, null=True, blank=True) 
    
    # Distrato
    observacao_distrato = models.TextField(max_length=250, null=True, blank=True)
    flag_distrato = models.BooleanField(default=False)
    anexo_distrato = models.FileField(upload_to='distrato/', null=True, blank=True)
    
    # Relacionamento com a classe PastaBiblioteca
    pasta_biblioteca = models.ForeignKey(PastaBiblioteca, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Relacionamento com a classe Categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Relacionamento com a classe Fornecedor
    nome_fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos de vigência
    data_criacao = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    data_inicio = models.DateField(null=True, blank=False)
    data_fim = models.DateField(null=True, blank=False)
    renovacao_automatica = models.BooleanField(default=False)

    # Imobilizado ou despesa
    tipo_gasto = models.CharField(max_length=12, choices=IMOBILIZADO_DESPESA_CHOICES, null=True, blank=True)
    
    # Centro de custos
    c_contabil = models.CharField(max_length=50, null=True, blank=True)
    centro_custo = models.CharField(max_length=100, null=True, blank=True)
    area_beneficiada = models.CharField(max_length=255, null=True, blank=True)
    
    # Observação do rateio
    observacao_rateio = models.TextField(max_length=500, null=True, blank=True)
    flag_rateio = models.BooleanField(default=False)
    
    # Forma de pagamento
    forma_pagamento = models.CharField(max_length=100, choices=FORMA_PAGAMENTO_CHOICES, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=False)
    observacao_valor = models.TextField(max_length=250, null=True, blank=True)
    observacao_pagamento = models.TextField(max_length=150, null=True, blank=True)
    
    # Reajustes
    indice_reajuste = models.CharField(max_length=100, choices=INDICE_REAJUSTE_CHOICES, null=True, blank=True)
    observacao_reajuste = models.CharField(max_length=250, null=True, blank=True)
    data_reajuste = models.DateField(null=True, blank=True)
    
    mention_users = models.ManyToManyField(User, related_name="mentioned_contratos", blank=True)
    criador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    visibilidade_privada = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.categoria and not self.c_contabil:
            self.c_contabil = self.categoria.c_contabil
        if not self.referencia_contrato:
            self.referencia_contrato = str(uuid.uuid4().int)[:5]
        if not self.criador:
            self.criador = kwargs.get('user')  
        if self.renovacao_automatica and self.data_fim:
            self.data_fim += timedelta(days=365)  # Prolonga por um ano se a renovação estiver ativada
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_fornecedor} - {self.referencia_contrato}"
    
    def get_contrato_url(self):
        if self.contrato_file:
            return self.contrato_file.url
        return None

    def get_imagem_url(self):
        if self.imagem:
            return self.imagem.url
        return None

class AccessLog(models.Model):
    path = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField()
    
class HistoricoContrato(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    campos_alterados = models.JSONField(blank=True, default=dict)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.acao} - {self.contrato} por {self.usuario} em {self.data}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profile_pics/", null=True, blank=True)

    def __str__(self):
        return self.user.username

class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensagem = models.CharField(max_length=255)
    lido = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notificação para {self.usuario.username}'