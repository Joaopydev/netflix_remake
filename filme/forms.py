#Classe de que tem como finalidade criar um usuario
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django import forms


#Formulário Padrão do Django
class FormHomePage(forms.Form):
    email = forms.EmailField(label=False)


#Sobre a class Meta: O Django vai criar um formulário, baseado nas configurações do meu modelo de usuário.
class FormCriarConta(UserCreationForm):
    email = forms.EmailField()  #required=False: Torna o campo como opicional

    class Meta:
        model = Usuario
        #fields: Define quais campos irão aparecer
        fields = ("username", "email", "password1", "password2")