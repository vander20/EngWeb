# Generated by Django 4.2.17 on 2024-12-13 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_perfil_foto_alter_perfil_cidade_alter_perfil_contato_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='descricao',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]