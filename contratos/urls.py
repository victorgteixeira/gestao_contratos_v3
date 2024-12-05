from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_contratos, name='listar_contratos'),
    path('adicionar/', views.adicionar_contrato, name='adicionar_contrato'),
    path('contratos/<int:contrato_id>/editar/', views.editar_contrato, name='editar_contrato'),
    path('visualizar/<int:id>/', views.visualizar_contrato, name='visualizar_contrato'),
    path('encerrar/<int:id>/', views.encerrar_contrato, name='encerrar_contrato'),
    path('adicionar_categoria/', views.adicionar_categoria, name='adicionar_categoria'),
    path('categorias/', views.listar_categoria, name='listar_categoria'),
    path('categoria/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('fornecedor/adicionar/', views.adicionar_fornecedor, name='adicionar_fornecedor'),
    path('fornecedores/', views.listar_fornecedores, name='listar_fornecedores'),
    path('fornecedor/editar/<int:fornecedor_id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('pastas_biblioteca/adicionar_pasta_biblioteca/', views.adicionar_pasta_biblioteca, name='adicionar_pasta_biblioteca'),
    path('pastas_biblioteca/', views.listar_pasta_biblioteca, name='listar_pasta_biblioteca'),
    path('pastas_biblioteca/editar/<int:pasta_id>/', views.editar_pasta_biblioteca, name='editar_pasta_biblioteca'),
    path('get_c_contabil/', views.get_c_contabil, name='get_c_contabil'),
    path('pastas_biblioteca/<int:pasta_id>/contratos/', views.visualizar_contratos_da_pasta, name='visualizar_contratos_da_pasta'),
    path('upload/', views.upload_file, name='upload_file'),
    path('buscar-fornecedor/', views.buscar_fornecedor, name='buscar_fornecedor'),
    path('buscar-fornecedor-cpf/', views.buscar_fornecedor_cpf, name='buscar_fornecedor_cpf'),
    path('buscar-fornecedor-nome/', views.buscar_fornecedor_nome, name='buscar_fornecedor_nome'),
    path('ajuda_buscar_fornecedor/', views.ajuda_buscar_fornecedor, name='ajuda_buscar_fornecedor'),
    path('contratos/contrato/<int:contrato_id>/historico/', views.historico_contrato, name='historico_contrato'),
    path('contrato/<int:id>/historico/', views.historico_contrato, name='historico_contrato'),
    path('config-usuario/', views.config_usuario, name='config_usuario'),
]

