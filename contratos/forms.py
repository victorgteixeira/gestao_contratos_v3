from django import forms
from .models import Contrato, Categoria, Fornecedor, PastaBiblioteca

class ContratoForm(forms.ModelForm):

    cnpj_fornecedor = forms.CharField(
        max_length=18, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Digite o CNPJ'})
    )
    cpf_fornecedor = forms.CharField(
        max_length=18, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Digite o CPF'})
    )
    id_nome_fornecedor_text = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Digite o nome do fornecedor'})
    )
    valor = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'R$ 0,00'}))
    
    class Meta:
        model = Contrato
        fields = ['nome_fornecedor', 'responsavel', 'categoria', 'c_contabil', 'observacao_contrato',
                  'area_beneficiada', 'data_inicio', 'data_fim', 'renovacao_automatica', 'pasta_biblioteca', 'tipo_gasto', 'centro_custo', 
                  'observacao_rateio', 'forma_pagamento', 'valor', 'observacao_valor', 'observacao_pagamento', 'visibilidade_privada', 
                  'indice_reajuste', 'observacao_reajuste', 'data_reajuste', 'status', 'contrato_file', 'imagem', 'observacao_distrato', 'flag_distrato', 'anexo_distrato', 'flag_rateio', 'cnpj_fornecedor','cpf_fornecedor']
        
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Se o contrato já existir
            self.fields['nome_fornecedor'].disabled = True
        
        # Tornando o campos obrigatório
        self.fields['nome_fornecedor'].required = True
        self.fields['responsavel'].required = True
        self.fields['categoria'].required = True
        self.fields['area_beneficiada'].required = True
        self.fields['data_inicio'].required = True
        self.fields['data_fim'].required = True
        self.fields['pasta_biblioteca'].required = True
        self.fields['tipo_gasto'].required = True
        self.fields['forma_pagamento'].required = True
        self.fields['valor'].required = True
        self.fields['indice_reajuste'].required = True
        self.fields['data_reajuste'].required = True
        
        # Configurando campos de data
        self.fields['data_inicio'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['data_fim'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['data_reajuste'].widget = forms.DateInput(attrs={'type': 'date'})
        
        # Configurando o campo 'responsavel' com placeholder do usuário logado
        if user:
            self.fields['responsavel'].widget.attrs['placeholder'] = f'{user.username}'
        
        # Personalizando campos de observação individualmente
        
        self.fields['observacao_contrato'].widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Observações específicas sobre o contrato',
                'rows': 4,
                'cols': 50
            }
        )
        
        self.fields['observacao_reajuste'].widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Detalhes sobre o reajuste do contrato',
                'rows': 4,
                'cols': 50
            }
        )
        
        self.fields['observacao_valor'].widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Informações relevantes sobre o valor acordado',
                'rows': 4,
                'cols': 50
            }
        )
        
        self.fields['observacao_pagamento'].widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Instruções ou observações sobre o pagamento',
                'rows': 4,
                'cols': 50
            }
        )
        
        self.fields['observacao_rateio'].widget = forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Observações sobre o rateio de despesas',
                'rows': 4,
                'cols': 50
            }
        )
        
    def clean_data_fim(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        data_fim = self.cleaned_data.get('data_fim')

        if data_fim and data_inicio and data_fim < data_inicio:
            raise forms.ValidationError("A data de fim deve ser maior ou igual à data de início.")
        return data_fim

    def clean(self):
        cleaned_data = super().clean()
        flag_distrato = cleaned_data.get("flag_rateio")
        centro_custo = cleaned_data.get("centro_custo")

        if not flag_distrato and not centro_custo:
            self.add_error('centro_custo', "Este campo é obrigatório quando o Rateio não está marcado.")
        return cleaned_data
    
    def clean_obs_rateio(self):
        cleaned_data = super().clean()
        flag_distrato = cleaned_data.get("flag_rateio")
        observacao_rateio = cleaned_data.get("observacao_rateio")

        if flag_distrato and not observacao_rateio:
            self.add_error('observacao_rateio', "Este campo é obrigatório quando o distrato está marcado.")

        return cleaned_data
    
    def clean_nome_fornecedor_text(self):
        nome_fornecedor = self.cleaned_data.get('nome_fornecedor_text')
        if nome_fornecedor:
            # Verifique se o fornecedor existe no banco de dados
            if not Fornecedor.objects.filter(nome=nome_fornecedor).exists():
                raise forms.ValidationError("Fornecedor não encontrado. Você pode precisar criá-lo primeiro.")
        return nome_fornecedor


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'c_contabil']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Prestação de Serviço'}),
            'c_contabil': forms.TextInput(attrs={'placeholder': 'Ex: 51460001 – Prestação de Serviço PJ​'}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nome'].required = True
        self.fields['c_contabil'].required = True
    
        
class AdicionarFornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'cpf', 'endereco']
        widgets = {
            'cnpj': forms.TextInput(attrs={'placeholder': 'Ex: 00.000.000/0000-00'}),
            'cpf': forms.TextInput(attrs={'placeholder': 'Ex: 000.000.000-00'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-500 focus:outline-none p-3 text-gray-900 bg-white'
            })
        
        self.fields['nome'].required = True
        self.fields['cnpj'].required = False
        self.fields['cpf'].required = False
        #self.fields['email'].required = False
        #self.fields['telefone'].required = False
        self.fields['endereco'].required = False


class PastaBibliotecaForm(forms.ModelForm):
    class Meta:
        model = PastaBiblioteca
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Documentos'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nome'].required = True
        
        
class UploadFileForm(forms.Form):
    file = forms.FileField()