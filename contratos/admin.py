from django.contrib import admin
from .models import Contrato, Categoria, Fornecedor, PastaBiblioteca, AccessLog

# Contratos
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('referencia_contrato', 'nome_fornecedor', 'categoria', 'responsavel', 'c_contabil', 'valor', 'area_beneficiada', 'status', 'data_criacao') 
    list_filter = ('categoria', 'status', 'data_criacao')  # Filtros na lateral
    search_fields = ('referencia_contrato', 'nome_fornecedor', 'responsavel')  # Campos pesquisáveis
    ordering = ('-data_criacao',)  # Ordenação por data de criação decrescente

admin.site.register(Contrato, ContratoAdmin)

# Categorias
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

admin.site.register(Categoria, CategoriaAdmin)

# Fornecedores
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'cpf', 'endereco')
    search_fields = ('nome', 'cnpj', 'cpf', 'endereco') 

admin.site.register(Fornecedor, FornecedorAdmin)

# Pasta Biblioteca
class PastabibliotecaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

admin.site.register(PastaBiblioteca, PastabibliotecaAdmin)

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('path', 'ip_address', 'timestamp', 'user_agent')
    list_filter = ('timestamp',)
    search_fields = ('path', 'ip_address', 'user_agent')
    ordering = ('-timestamp',)

    actions = ['delete_old_logs']

    @admin.action(description='Deletar logs com mais de 10 dias')
    def delete_old_logs(self, request, queryset):
        from datetime import timedelta
        from django.utils.timezone import now

        cutoff_date = now() - timedelta(days=10)
        deleted_count, _ = AccessLog.objects.filter(timestamp__lt=cutoff_date).delete()
        self.message_user(request, f'{deleted_count} registros antigos foram deletados com sucesso.')

