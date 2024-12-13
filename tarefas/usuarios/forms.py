from django import forms
from django.contrib.auth.models import User
from .models import Perfil, SolicitacaoServico, Avaliacao

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário',
                'maxlength': 150,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-mail',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Senha',
            }),
        }
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'password': 'Senha',
        }
        help_texts = {
            'username': 'Escolha um nome de usuário. Apenas letras, números e @/./+/-/_ são permitidos.',
        }
        error_messages = {
            'username': {
                'required': 'Por favor, informe um nome de usuário.',
                'max_length': 'O nome de usuário não pode exceder 150 caracteres.',
            },
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['funcao', 'contato', 'cidade', 'foto', 'descricao']
        labels = {
            'funcao': 'Tipos de Serviços Prestados',
            'contato': 'Informações de Contato',
            'cidade': 'Cidade',
            'foto': 'Foto de Perfil',
            'descricao': 'Descrição (Experiência e Habilidades)',
        }
        widgets = {
            'funcao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite os serviços que você presta',
                'rows': 3,
                'style': 'resize: none;',
            }),
            'contato': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu contato',
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua cidade',
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva suas experiências e habilidades',
                'rows': 5,
                'style': 'resize: none;',
            }),
        }

class SolicitacaoServicoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoServico
        fields = ['mensagem']
        labels = {
            'mensagem': 'Mensagem para o prestador de serviço',
        }
        widgets = {
            'mensagem': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva sua solicitação para o prestador de serviço',
                'rows': 4,
                'style': 'resize: none;',
            }),
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota']
        labels = {
            'nota': 'Nota',
        }
        widgets = {
            'nota': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
