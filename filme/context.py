#Esse arquivo é uma estrutura de context - Que vai replicar a variável context par todas as views do site
from .models import Filme

#Precisa definir um função que recebe o request como parâmetro. Lembrando uma function base views
#Essa função vai retornar o context como resposta, ou seja, uma variável para as páginas HTML
#A resposta da função precisa ser um dicionário -  Onde a chave vai representar o valor nas páginas HTML
def lista_filmes_recentes(request):
    #Pegando a lista de filme e ordenando a partir de sua data de criação, em ordem descrecente, por causa do "-" antes do nome da coluna do banco de dados que foi usada como referencia para ordenar a lista.
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:8]
    return {"lista_filmes_recentes": lista_filmes }

def lista_filmes_alta(request):
    lista_filmes = Filme.objects.all().order_by('-views')[0:8]
    return {"lista_filmes_alta": lista_filmes}


#Não esquecer que para essas variáveis funcionarem nos nossos HTML| Também precisam ser configuradas na variável TEMPLATES no arquivo settings.py na pasta principal
#Implementação é feita no parâmetro context_processors. Sintaxe: "nomedoapp.NomeDoArquivoOndeEstáAfunção.NomeDaFunção"
#Exemplificando:"filme.context.lista_filmes_alta "