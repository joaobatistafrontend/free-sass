from django import forms
from .models import *

class ProfissionalForm(forms.ModelForm):
    class Meta:
        model = Profissional
        fields = ['nome', 'especialidade']  # Adicione outros campos conforme necessário

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'duracao', 'preco']  # Adicione outros campos conforme necessário

class HorarioAtendimentoForm(forms.ModelForm):
    class Meta:
        model = HorarioAtendimento
        fields = ['dia_semana', 'hora_abertura', 'hora_fechamento']

class MensagemAniversarioForm(forms.ModelForm):
    class Meta:
        model = MensagemAniversario
        fields = ['mensagem']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'numero_whatsapp', 'data_aniversario']        