from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cidade = models.CharField(max_length=100)
    funcao = models.CharField(max_length=100)
    contato = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='fotos_perfil/', default='fotos_perfil/default.png')
    descricao = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class SolicitacaoServico(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitacoes')
    prestador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicos')
    mensagem = models.TextField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('aceito', 'Aceito'),
            ('recusado', 'Recusado'),
            ('concluido', 'Concluído'),
        ],
        default='pendente'
    )

    def __str__(self):
        return f"Solicitação de {self.cliente.username} para {self.prestador.username}"


class Avaliacao(models.Model):
    avaliador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='avaliacoes_feitas'
    )  # Usuário que faz a avaliação
    prestador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='avaliacoes_recebidas'
    )  # Usuário que recebe a avaliação
    nota = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],  # Notas de 1 a 5
        verbose_name="Nota"
    )
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.avaliador.username} para {self.prestador.username} - Nota: {self.nota}"
