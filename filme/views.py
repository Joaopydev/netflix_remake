from django.shortcuts import redirect, reverse
from .models import Filme, Usuario
#TemplateView: Quando Objetivo é apenas renderizar uma página HTML na classe.
#ListView: Quando o Objetivo é exibir uma Lista de Itens do banco de dados.
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
#Importação que será passada para a class base view, para bloquear aquela rota apenas para usuários autenticados.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import FormCriarConta, FormHomePage
# Create your views here.

#template_name: Váriavel Padrão da Classe TemplateView do Django, usada para determinar a página HTML que vai ser renderizada.
class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomePage

    def get(self, request, *args, **kwargs):
        #Verifica se o usuário está autenticado
        #Caso ele estja autenticado eu vou redireciona-lo para a página de filmes
        if request.user.is_authenticated:
            return redirect("filme:homefilmes")
        #Caso contrário, continuar retornando a página html padrão que é a homepage
        else:
            return super().get(request, *args, **kwargs)

    #Pegando o email da requisição POST que o usuário está fazendo na página Home
    def get_success_url(self):
        email = self.request.POST.get("email")
        #Caso o email exista, retornar página de login
        usuario = Usuario.objects.filter(email=email).first()
        if usuario:
            return reverse("filme:login")
        #Caso nao exista retorna página de criar conta
        else:
            return reverse("filme:criarconta")

#Fax todoo o processo de criação de contexto automáticamente - Como foi feito na Functions Base Views Anteriormente
class HomeFilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    #Cria uma lista da tabela "Filme" do banco de dados e retorna a variável "object_list" para página html em que está implementada.
    model = Filme #object_list -> Lista os itens do modelo

#Por padrão passar as mesmas variáveis que um ListView.
#DetailView: Cria um página para cada filme que existe no banco de dados - Exibindo os seus detalhes.

#Quando for necessário passar uma variável para dentro de umaview específica, é preciso alterar a variável:
#def get_context_data(self, **kwargs) - Que caso essa função vai possibilitar adicionar um valor na variável context
#context = super(DetalhesFilme, self).get_context_data(**kwargs) - Para não sobreescrever as funcionalidade dessa função da classe mas sim adicionar um valor nela.
class DetalhesFilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme #object -> 1 Item do modelo

    #Definindo a função get, onde vai ser criado a lógica de contabilizar as visualizações de cada filme.
    #O real motivo é contabilizar quantas vezes os usuários dão um click em uma página. Ou seja quando o usuário da um "get" na página
    #Parâmetro padrões: request, *args, **kwargs
    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.views += 1
        #Salva o valor que foi adicionado a coluna views
        filme.save()
        #Adicionar o filme que o usuário clicou para ver na lista de filmes_vistos do usuário atual
        user = request.user
        user.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetalhesFilme, self).get_context_data(**kwargs)
        #Filtrar a tabela de filmes, cujo as categorias são iguais as categorias do filme da página
        #self.get_object() - Usado para pegar a variável object
        #[0:5] Para limitar a lista, ou seja, pegar primeiro item até o quinto item.
        filmes_relacionados = self.model.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados #A variável no HTML sempre será a chave do que foi definida
        return context


class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    #get_queryset: Serve para pegar os parâmetros da minha query/busca. E a partir disso, dizer quais informações seram passadas para o object_list.
    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            #titulo__icontains: Vai verificar se o texto que foi passado como parâmetro, está contido no titulo. Ou essa verificação poderia ser feita por outra coluna da tabela, como a descrição, por exemplo.
            object_list = self.model.objects.filter(titulo__icontains=query)
            return object_list
        else:
            return None

#UpdateView: Classe utilizada para realizar uma atualização no banco de dados baseado no modelo que você passa.
#fields: Diz Quais campos do banco de dados o usuário vai poder atualizar
#UserPassesTestMixin: Previnir para que apenas o request_user, tenha autorização para alterar o prórpio perfil
class EditarPerfil(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ["first_name", "last_name", "email"]

    #Retorna apenas o usuário que é o próprio usuário da requisição atual
    def test_func(self):
        user = self.get_object()
        return self.request.user == user

    def get_success_url(self):
        return reverse("filme:homefilmes")



class CriarConta(FormView):
    template_name = "criarconta.html"
    form_class = FormCriarConta

    #form_valid: Editando essa função para que o formulário seja salvo efitivamente no banco de dados
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    #Retorna o usuário para uma determinada página, caso a criação de conta tenha sido feita com sucesso
    #reverse: Utilizar quando a função pede como resposta um texto de link, ele pega o link correspondente ao html que foi pasasdo como parâmetro
    def get_success_url(self):
        return reverse("filme:login")