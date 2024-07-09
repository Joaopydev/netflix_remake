"""
URL configuration for cursosflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#namespace é usado para agrupar URLs sob um prefixo comum, o que é útil para evitar conflitos de nome quando você tem várias aplicações que podem ter rotas com nomes iguais.
#Basicamente ele identifica o arquivo url.py do app exato que ele precisa pegar, cujo a variável "app_name" possui o mesmo nome que foi passado como parâmetro para a variável "namespace"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('filme.urls', namespace='filme')),
]
#urls para os arquivos estáticos
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urls para os arquivos de mídia
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)