from django.db import models
#Essa importação do django é para trabalhar com horas
from django.utils import timezone
#Importação para criar o modelo de usuário - Usuário padrão do Django
from django.contrib.auth.models import AbstractUser

# Create your models here.
#Categorias para a coluna "categorias" - Necessáriamente precisa ser uma tupla.
#(Primeiro parâmetro: Vai aparecer no banco de dados, Segundo parâmetro: Vai aparecer pros usuários)
LISTA_CATEGORIAS = (
    ("ANALISES", "Análises"),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTACAO", "Apresentação"),
    ("OUTROS", "Outros")
)
#Criar o filme
class Filme(models.Model):
    #Cria as colunas da tabela Filme do banco de dados
    #Titulo -  models.CharField - Indica que essa coluna será do tipo string | max_lenght - Definindo a quantidade de caracteres.
    titulo = models.CharField(max_length=100)
    #Thumb - upload_to - É passado para esse parâmetro onde vão ficar armazenados as imagens dos filmes à medida que forem criados
    thumb = models.ImageField(upload_to="thumb_filmes")
    #Descricao - models.TextField - Mesma coisa que o CharField. Porém serve para textos grandes.
    descricao = models.TextField(max_length=1000)
    #choices - Parâmetro que vai armazenar a lista de categorias para o bd
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    views = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)

    #Essa função nativa do python - Define o que vai aparecer pro usuário quando ele der um print em algum item da Classe em que ele está definido.
    def __str__(self):
        return self.titulo


#Criar os episódios
#models.ManyToManYField - Cria uma relação muitiplas entre as tabelas, ou seja, muitos p/ muitos
class Episodio(models.Model):
    #related_name - É o que de fato faz eu conseguir referenciar no código os episódios que estão relacionados a um determinado filme.
    #on_delete=models.CASCADE - Basicamente ele cria a funcionalidade de excluir todos os episódios relacionados a um filme, caso o filme seja excluido
    filme = models.ForeignKey("Filme", related_name="episodios", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=140)
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo + " - " + self.titulo


#Criando a classe padrão de usuários do django - Ela herda todas as características já existentes nele - Aqui só é preciso colocar o que queremos acrescentar.
class Usuario(AbstractUser):
    #Criando a relação "Muito p/ Muitos" entre as classes, Usuário e Filme.
    filmes_vistos = models.ManyToManyField("Filme")


#Para realmente criar o modelo de Usuário 4 passos precisam ser seguidos
#1°: Criar no Modelo de usuário no arquivo models.py do app
#2°: Registrar o Modelo no admin.py, com um parâmetro adicional, que é o UserAdmin - Que basicamente diz pro django qual classe vai gerenciar os usuários.
#3°: Passar o Modelo para settings.py, com a variável: AUTH_USER_MODEL = "nome_do_app.Usuario".
#4°: Adicionar os campos personalizados no fields do UserAdmin
#OBS: Sempre fazer isso no início da criação do site