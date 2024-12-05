from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Contrato, Fornecedor, Categoria, PastaBiblioteca, HistoricoContrato, Notificacao  
from .forms import ContratoForm, CategoriaForm, AdicionarFornecedorForm, PastaBibliotecaForm
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from .forms import UploadFileForm
import pandas as pd
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Profile

# Contratos -------------------------------------------------------------------------------------------------
@login_required
def lista_contratos(request):
    busca = request.GET.get('busca', '')
    minhas_requisicoes = request.GET.get('minhas_requisicoes') == 'true'
    status = request.GET.get('status')

    if request.user.is_superuser:
        contratos = Contrato.objects.all().order_by('id')
    else:
        contratos = Contrato.objects.filter(
            Q(visibilidade_privada=False) | Q(criador=request.user)
        ).order_by('id')

    if busca:
        contratos = contratos.filter(
            Q(nome_fornecedor__nome__icontains=busca) | 
            Q(nome_fornecedor__cnpj__icontains=busca) |
            Q(referencia_contrato__icontains=busca) |
            Q(responsavel__icontains=busca)
        )
    
    if minhas_requisicoes:
        contratos = contratos.filter(criador=request.user)

    if status == 'ativo':
        contratos = contratos.filter(status='ativo')
    elif status == 'inativo':
        contratos = contratos.filter(status='encerrado')
    
    contratos_recente = contratos.order_by('-data_criacao')[:2]

    paginator = Paginator(contratos, 7) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, 'contratos/listar_contratos.html', {
        'contratos': contratos,
        'busca': busca,
        'minhas_requisicoes': minhas_requisicoes,
        'status': status,
        'page_obj': page_obj,
        'contratos_recente': contratos_recente
    })

@login_required
def adicionar_contrato(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            novo_contrato = form.save(commit=False)
            novo_contrato.criador = request.user
            novo_contrato.responsavel = form.cleaned_data['responsavel']
            novo_contrato.save()
            

            usuarios = User.objects.all()  # Todos os usuários cadastrados
            for usuario in usuarios:
                Notificacao.objects.create(usuario=usuario, mensagem="Novo contrato criado.")
            
            messages.success(request, 'Contrato criado com sucesso!')
            return redirect('listar_contratos')
    else:
        form = ContratoForm(user=request.user)
    
    return render(request, 'contratos/adicionar_contrato.html', {'form': form})

@login_required
def ajuda_buscar_fornecedor(request):
    query = request.GET.get('query', '')
    fornecedores = Fornecedor.objects.filter(nome__icontains=query)[:10]  # Limita a 10 sugestões
    results = [{'id': fornecedor.id, 'nome': fornecedor.nome} for fornecedor in fornecedores]
    return JsonResponse(results, safe=False)

from django.contrib import messages

@login_required
def editar_contrato(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)
    
    dados_anteriores = {field.name: getattr(contrato, field.name) for field in Contrato._meta.fields}

    if request.method == 'POST':
        form = ContratoForm(request.POST, request.FILES, instance=contrato)
        if form.is_valid():
            form.save()

            campos_alterados = []
            for campo in dados_anteriores.keys():
                if campo in form.cleaned_data and dados_anteriores[campo] != form.cleaned_data[campo]:
                    campos_alterados.append(f"{campo}: {dados_anteriores[campo]} → {form.cleaned_data[campo]}")

            HistoricoContrato.objects.create(
                contrato=contrato,
                acao='Atualizado',
                campos_alterados=', '.join(campos_alterados),
                usuario=request.user
            )

            messages.success(request, 'Alterações realizadas com sucesso!')
            return redirect('listar_contratos')
        else:
            messages.error(request, 'Ocorreu um erro ao processar sua solicitação.')
            print(form.errors)

    else:
        # Preenche o campo `nome_fornecedor` automaticamente com o valor do contrato
        form = ContratoForm(instance=contrato, initial={'nome_fornecedor': contrato.nome_fornecedor})

    return render(request, 'contratos/editar_contrato.html', {'form': form, 'contrato': contrato})

@login_required
def visualizar_contrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    return render(request, 'contratos/visualizar_contrato.html', {'contrato': contrato})
    
@login_required
def encerrar_contrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    if contrato.status == 'encerrado':
        messages.warning(request, f'O contrato {contrato.referencia_contrato} já está encerrado.')
        return redirect('listar_contratos')
    contrato.status = 'encerrado'
    contrato.save()
    messages.success(request, f'O contrato {contrato.referencia_contrato} foi encerrado com sucesso.')
    return redirect('listar_contratos')

@login_required
def historico_contrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    alteracoes = HistoricoContrato.objects.filter(contrato=contrato).order_by('-data')

    return render(request, 'contratos/historico_contrato.html', {
        'contrato': contrato,
        'alteracoes': alteracoes
    })

    
# Categorias-------------------------------------------------------------------------------------------------
@login_required
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria adicionada com sucesso.')
            return redirect('listar_categoria')
    else:
        form = CategoriaForm()
    
    return render(request, 'categorias/adicionar_categoria.html', {'form': form})

@login_required
def listar_categoria(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/listar_categoria.html', {'categorias': categorias})

@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria foi editada com sucesso!')
            return redirect('listar_categoria')
    else:
        form = CategoriaForm(instance=categoria)
        
    return render(request, 'categorias/editar_categoria.html', {'form': form, 'categoria': categoria})

# Fornecedores -----------------------------------------------------------------------------------------------

@login_required
def adicionar_fornecedor(request):
    if request.method == 'POST':
        form = AdicionarFornecedorForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor adicionado com sucesso!')
            return redirect('listar_fornecedores')
    else:
        form = AdicionarFornecedorForm()
    
    return render(request, 'fornecedores/adicionar_fornecedor.html', {'form': form})

@login_required
def listar_fornecedores(request):
    query = request.GET.get('query', '')
    order = request.GET.get('order', 'asc') 
    fornecedores = Fornecedor.objects.all()

    if query:
        fornecedores = fornecedores.filter(
            Q(nome__icontains=query) | Q(cnpj__icontains=query)
        )

    if order == 'asc':
        fornecedores = fornecedores.order_by('nome')
    elif order == 'desc':
        fornecedores = fornecedores.order_by('-nome')

    paginator = Paginator(fornecedores, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'fornecedores/listar_fornecedores.html', {
        'page_obj': page_obj,
        'query': query,
        'order': order,
    })
    
@login_required
def editar_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    
    if request.method == 'POST':
        form = AdicionarFornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor editado com sucesso')
            return redirect('listar_fornecedores')  
    else:
        form = AdicionarFornecedorForm(instance=fornecedor)
    
    return render(request, 'fornecedores/editar_fornecedor.html', {'form': form, 'fornecedor': fornecedor})

# Bibliotecas ------------------------------------------------------------------------------------------------
@login_required
def adicionar_pasta_biblioteca(request):
    if request.method == 'POST':
        form = PastaBibliotecaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pasta adicionada com sucesso!')
            return redirect('listar_pasta_biblioteca')
    else:
        form = PastaBibliotecaForm()
    
    return render(request, 'bibliotecas/adicionar_pasta_biblioteca.html', {'form': form})

@login_required
def listar_pasta_biblioteca(request):
    search_query = request.GET.get('search', '')

    if search_query:
        pastas = PastaBiblioteca.objects.filter(nome__icontains=search_query)
    else:
        pastas = PastaBiblioteca.objects.all()

    return render(request, 'bibliotecas/listar_pasta_biblioteca.html', {'pastas': pastas})

@login_required
def editar_pasta_biblioteca(request, pasta_id):
    pasta = get_object_or_404(PastaBiblioteca, id=pasta_id)

    if request.method == 'POST':
        form = PastaBibliotecaForm(request.POST, instance=pasta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pasta foi editada com sucesso!')
            return redirect('listar_pasta_biblioteca')
    else:
        form = PastaBibliotecaForm(instance=pasta)

    return render(request, 'bibliotecas/editar_pasta_biblioteca.html', {'form': form, 'pasta': pasta})

@login_required
def visualizar_contratos_da_pasta(request, pasta_id):
    pasta = get_object_or_404(PastaBiblioteca, id=pasta_id)

    contratos = Contrato.objects.filter(pasta_biblioteca=pasta)

    return render(request, 'bibliotecas/visualizar_contratos_da_pasta.html', {
        'pasta': pasta,
        'contratos': contratos
    })

# Coletar dados contabil --------------------------------------------------------------------------------------
@login_required
def get_c_contabil(request):
    categoria_id = request.GET.get('categoria_id')
    c_contabil = None
    if categoria_id:
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            c_contabil = categoria.c_contabil
        except Categoria.DoesNotExist:
            pass
    return JsonResponse({'c_contabil': c_contabil})

# Upload ------------------------------------------------------------------------------------------------------
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                df = pd.read_excel(request.FILES['file'])

                for index, row in df.iterrows():
                    try:
                        fornecedor = Fornecedor(
                            nome=row['nome'],
                            cnpj=row['cnpj'],
                            endereco=row['endereco'],
                        )
                        fornecedor.full_clean()
                        fornecedor.save()
                    except Exception as e:
                        messages.error(request, f'Erro ao salvar fornecedor na linha {index + 1}: {str(e)}')
                        continue 

                messages.success(request, 'Fornecedores carregados com sucesso!')
                return redirect('listar_fornecedores')

            except Exception as e:
                messages.error(request, f'Erro ao ler o arquivo: {str(e)}')
                return render(request, 'uploads/upload.html', {'form': form})

    else:
        form = UploadFileForm()
    return render(request, 'uploads/upload.html', {'form': form})

# Buscas ------------------------------------------------------------------------------------------------------
@login_required
def buscar_fornecedor(request):
    cnpj = request.GET.get('cnpj')
    fornecedor = Fornecedor.objects.filter(cnpj=cnpj).first()
    if fornecedor:
        data = {
            'id': fornecedor.id,
            'nome': fornecedor.nome,
        }
    else:
        data = {}
    return JsonResponse(data)

@login_required
def buscar_fornecedor_cpf(request):
    cpf = request.GET.get('cpf')
    fornecedor = Fornecedor.objects.filter(cpf=cpf).first()
    if fornecedor:
        data = {
            'id': fornecedor.id,
            'nome': fornecedor.nome,
        }
    else:
        data = {}
    return JsonResponse(data)

@login_required
def buscar_fornecedor_nome(request):
    nome = request.GET.get('nome')
    fornecedor = Fornecedor.objects.filter(nome__icontains=nome).first()
    if fornecedor:
        data = {
            'id': fornecedor.id,
            'cnpj': fornecedor.cnpj,
            'cnpj': fornecedor.cpf,
        }
    else:
        data = {}
    return JsonResponse(data)

@login_required
def config_usuario(request):
    user = request.user
    
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        if 'photo' in request.FILES:
            user.profile.photo = request.FILES['photo']
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
        user.save()
        return redirect('home') 
    
    return render(request, 'config_usuario.html')
