from django import template
import locale

register = template.Library()

@register.filter
def moeda(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
