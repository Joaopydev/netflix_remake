# url - view - template
from django.urls import path, reverse_lazy
#reverse_lazy: Passado pro path para retornar o link da página que o usuário vai entrar ao submeter o formulário
from .views import HomeFilmes, Homepage, DetalhesFilme, Pesquisafilme, EditarPerfil, CriarConta
#Importação para pegar a classe de Login que já vem pronta do Django
from django.contrib.auth import views as auth_view

#app_name é usada dentro dos arquivos urls.py de um aplicativo para definir um namespace próprio para esse conjunto de URLs.
app_name = "filme"

#Para Functions Base Views: Passar o nome da função como parâmetro o Django já vai entender que queremos renderizar a página HTML que está definida na função
#Para Class Base Views: Necessário passar NomeDaClasse.as_view() - "()" É obrigatório passar.

#A criação do link de página que renderiza uma DetailView é diferente:
#Ele espera que tenha um parâmetro na url dentro de "< >" - E também precisa informar o tipo desse parâmetro. Ex: int, float, str...
#No exemplo foi utilizado "int:pk" onde "pk" é a primary key da tabela que foi implementada na DetailView
#Ele faz essa busca automaticamente - Tendo em mente que foi definida a tabela do banco de dados que vamos renderizar
urlpatterns = [
    path('', Homepage.as_view(), name="homepage"),
    path('filmes/', HomeFilmes.as_view(), name="homefilmes"),
    path('filmes/<int:pk>', DetalhesFilme.as_view(), name="detalhesfilme"),
    path('pesquisa/', Pesquisafilme.as_view(), name="pesquisafilme"),
    #template_name: Para o Django diferenciar os HTML's das views que possuem a classe pronta do Django.
    path('login/', auth_view.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path('editar-perfil/<int:pk>', EditarPerfil.as_view(), name="editarperfil"),
    path('criar-conta/', CriarConta.as_view(), name="criarconta"),
    path('alterar-senha/', auth_view.PasswordChangeView.as_view(template_name="editarperfil.html",
                                                                success_url=reverse_lazy('filme:homefilmes')), name="mudarsenha")
]

#o parâmetro name usado nas rotas (URLs) serve para dar um nome único a cada rota, permitindo que você se refira a essas rotas d    e uma maneira mais fácil e robusta em todo o seu código.