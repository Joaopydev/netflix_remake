from django.contrib import admin
#Significado do "." antes do models é que eu estou dizendo que quero importar o arquivo models qu está na mesma pasta do meu arquivo admin.py
from .models import Filme, Episodio, Usuario
#Importação para dizer pro django a classe que vai fazer o gerenciamento dos usuário - Que no caso é o modelo de Usuário.
from django.contrib.auth.admin import UserAdmin

# Register your models here.

#Isso só é necessário pela necessidade de adicionar os campos personalizados no database.
#Tem como funcionalidade real - Fazer esse acampo aparecer no banco de dados.
#OBS: Quando for repetir em outro projeto, utilizar exatamente a mesma sintaxe
campos = list(UserAdmin.fieldsets)
campos.append(
    ("Histórico", {"fields": ("filmes_vistos",)})
)
UserAdmin.fieldsets = tuple(campos)

#Codigo para registrar a tabela do bd no site do admin.
admin.site.register(Filme)
admin.site.register(Episodio)
admin.site.register(Usuario, UserAdmin)
