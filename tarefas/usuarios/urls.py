from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),  # Nova página inicial
    path('home/', views.usuarios_home, name='usuarios_home'),  # Página Home atualizada
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar/', views.editar_perfil, name='editar_perfil'),
    path('buscar/', views.buscar_usuarios, name='buscar_usuarios'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/<int:perfil_id>/', views.perfil_detalhado, name='perfil_detalhado'),  # Rota para perfil detalhado
    path('solicitacao/<int:perfil_id>/', views.enviar_solicitacao, name='enviar_solicitacao'),  # Rota para solicitação de serviços
    path('avaliacao/<int:perfil_id>/', views.deixar_avaliacao, name='deixar_avaliacao'),
    path('perfil/', views.perfil, name='perfil'),
  # Rota para avaliação
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
