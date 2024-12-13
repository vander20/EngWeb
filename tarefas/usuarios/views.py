from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserForm, PerfilForm, SolicitacaoServicoForm, AvaliacaoForm
from .models import Perfil, SolicitacaoServico, Avaliacao

class RegistroView(View):
    def get(self, request):
        user_form = UserForm()
        perfil_form = PerfilForm()
        return render(request, 'usuarios/registro.html', {
            'user_form': user_form,
            'perfil_form': perfil_form,
        })

    def post(self, request):
        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST, request.FILES)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            return redirect('login')
        return render(request, 'usuarios/registro.html', {
            'user_form': user_form,
            'perfil_form': perfil_form,
        })

def pagina_inicial(request):
    return render(request, 'usuarios/pagina_inicial.html')

@login_required
def perfil(request):
    try:
        perfil = Perfil.objects.get(user=request.user)
        solicitacoes_enviadas = SolicitacaoServico.objects.filter(cliente=request.user).distinct()
        solicitacoes_recebidas = SolicitacaoServico.objects.filter(prestador=request.user).distinct()
        avaliacoes_recebidas = Avaliacao.objects.filter(prestador=request.user).order_by('-data_avaliacao')
    except Perfil.DoesNotExist:
        return render(request, 'usuarios/perfil_nao_encontrado.html')

    # Extraindo apenas as notas para exibição
    notas = avaliacoes_recebidas.values_list('nota', flat=True)

    return render(request, 'usuarios/perfil.html', {
        'perfil': perfil,
        'solicitacoes_enviadas': solicitacoes_enviadas,
        'solicitacoes_recebidas': solicitacoes_recebidas,
        'notas': notas,  # Passa as notas para o template
    })



def buscar_usuarios(request):
    query = request.GET.get('q')
    if query:
        resultados = Perfil.objects.filter(
            Q(funcao__icontains=query) | Q(cidade__icontains=query)
        )
    else:
        resultados = []
    return render(request, 'usuarios/buscar.html', {
        'resultados': resultados,
    })

@login_required
def usuarios_home(request):
    return render(request, 'usuarios/home.html')

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin/'
        return '/usuarios/home/'

@login_required
def editar_perfil(request):
    try:
        # Busca o perfil do usuário logado
        perfil = Perfil.objects.get(user=request.user)
    except Perfil.DoesNotExist:
        # Cria um perfil vazio associado ao usuário, caso não exista
        perfil = Perfil(user=request.user)
        perfil.save()

    if request.method == 'POST':
        # Vincula o formulário ao perfil existente
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            # Redireciona para o perfil após salvar as alterações
            return redirect('perfil')
        else:
            # Exibe erros de validação, caso existam
            print(form.errors)
    else:
        # Carrega o formulário com os dados do perfil existente
        form = PerfilForm(instance=perfil)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})


def perfil_detalhado(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    avaliacoes = Avaliacao.objects.filter(prestador=perfil.user)
    return render(request, 'usuarios/perfil_detalhado.html', {
        'perfil': perfil,
        'avaliacoes': avaliacoes,
    })

def perfil_detalhado(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)  # Busca o perfil pelo ID ou retorna 404
    avaliacoes_recebidas = Avaliacao.objects.filter(prestador=perfil.user).order_by('-data_avaliacao')

    if request.method == 'POST':
        form = SolicitacaoServicoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.cliente = request.user
            solicitacao.prestador = perfil.user
            solicitacao.save()
            return redirect('perfil_detalhado', perfil_id=perfil.id)
    else:
        form = SolicitacaoServicoForm()

    # Extraindo apenas as notas para exibição
    notas = avaliacoes_recebidas.values_list('nota', flat=True)

    return render(request, 'usuarios/perfil_detalhado.html', {
        'perfil': perfil,
        'form': form,
        'notas': notas,  # Passa as notas para o template
    })


@login_required
def enviar_solicitacao(request, perfil_id):
    prestador = get_object_or_404(User, perfil__id=perfil_id)
    if request.method == 'POST':
        form = SolicitacaoServicoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.cliente = request.user
            solicitacao.prestador = prestador
            solicitacao.save()
            return redirect('perfil_detalhado', perfil_id=perfil_id)
    else:
        form = SolicitacaoServicoForm()
    return render(request, 'usuarios/solicitacao.html', {'form': form, 'prestador': prestador})

@login_required
def deixar_avaliacao(request, perfil_id):
    prestador = get_object_or_404(User, perfil__id=perfil_id)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.avaliador = request.user
            avaliacao.prestador = prestador
            avaliacao.save()
            messages.success(request, 'Avaliação enviada com sucesso!')
            return redirect('perfil_detalhado', perfil_id=perfil_id)
        else:
            messages.error(request, 'Erro ao salvar a avaliação.')
    else:
        form = AvaliacaoForm()
    return render(request, 'usuarios/deixar_avaliacao.html', {'form': form, 'prestador': prestador})

def logout_view(request):
    logout(request)
    return redirect('pagina_inicial')
