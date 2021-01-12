"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
   
    #path('importe', views.importe),
  
    #path('zoom/', views.zoom, name='zoom'),
    path('zoom/<slug:categorie>/<slug:date_projet>/<slug:thumb>', views.zoom, name='zoom'),
  
    #path('admin/', admin.site.urls),
    path('category/exhibitions/', views.exhibitions, name='exhibitions'),
    path('category/projects/', views.projects, name='projects'),
    path('category/publications/', views.publications, name='publications'),
    path('category/videos/', views.videos, name='videos'),
    path('contact/', views.contact, name='contact'),
    path('index/', views.index,name='index'),
    path('', views.index,name='index'),
    path('cv/', views.cv,name='cv'),
    path('exhibitions/', views.exhibitions, name='exhibitions/'),
    path('publications/', views.publications, name='publications/'),
    path('projects/', views.projects, name='projects'),
    path('vigvideo/<slug:categorie>/<slug:date_projet>', views.vigvideo, name='vigvideo'),
    path('videos/', views.videos, name='videos/'),    
    path('video__player/<slug:lien>/<slug:untitreesp>', views.video__player, name='video__player'),
    path('object/<slug:date_projet>/<slug:projet>/<slug:categorie>', views.projet, name='object'),  
    path('projet/<slug:date_projet>/<slug:projet>/<slug:categorie>', views.projet, name='projetslug'),  
    path('trumbo/<slug:lien>', views.trumbo, name='trumbo'),  
    path('trumbo/', views.trumbo, name='trumbo'),  
    path('upload/<kiwcom>', views.upload,name='upload'),
    path('vcaadmin/<var>', views.vcaadmin,name='vcaadmin'),
    path('filesave/<slug:lien>/<slug:data>', views.filesave, name='filesave'), 
    path('myadmin/', views.myadmin,name='myadmin'),
    path('textareasub/', views.textareasub,name='textareasub'),
    path('creation/', views.creation,name='creation'),
    path('eff_proj/<slug:dossier>/<slug:projet>', views.eff_proj,name='eff_proj'),
    path('visiteurs_liste/', views.visiteurs_liste,name='visiteur_liste'),
    path('merci/', views.merci,name='merci'),
    path('sauve_visiteur/', views.sauve_visiteur,name='sauve_visiteur'),
    path('myhelp/', views.myhelp,name='myhelp'),
    path('upphocv/', views.upphocv,name='upphocv'),
    path('upphocont/', views.upphocont,name='upphocont'),
    path('htmltxt/<slug:dossier>', views.htmltxt,name='htmltxt'),
    path('deschtm2txt/', views.deschtm2txt,name='deschtm2txt'),
    path('titlehtm2txt/', views.titlehtm2txt,name='titlehtm2txt'),
    path('metatest/', views.metatest,name='metatest'),
    path('publicationstest/', views.publicationstest, name='publicationstest/'),
  
    
    #TODO: devier oject sur projet pur garder lesliens existants
   
]


