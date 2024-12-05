from django.shortcuts import render
from django.db.models import Sum
from contratos.models import Contrato
from django.contrib.auth.decorators import login_required

@login_required
def top_contratos_view(request):
    top_contratos = Contrato.objects.order_by('-valor')[:10]
    
    # Agrupa por categoria e soma os valores para cada categoria
    categoria_gastos = (
        Contrato.objects
        .values('categoria__nome')
        .annotate(total_valor=Sum('valor'))
        .order_by('-total_valor')[:10]
    )
    
    # Agrupa por fornecedor e soma os valores para cada fornecedor
    fornecedor_gastos = (
        Contrato.objects
        .values('nome_fornecedor__nome')
        .annotate(total_valor=Sum('valor'))
        .order_by('-total_valor')[:10]
    )

    context = {
        'top_contratos': top_contratos,
        'categoria_gastos': categoria_gastos,
        'fornecedor_gastos': fornecedor_gastos,
    }
    return render(request, 'dashboard/top_contratos.html', context)
