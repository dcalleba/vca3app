#!/usr/bin/python
# coding: utf-8
from __future__ import unicode_literals
#from bs4 import BeautifulSoup
from html.parser import HTMLParser
import html
import os
import sys
# sys.path.append('/home/dcallebaut/apps/vcaapp/myproject/myproject')

from datetime import date
#from django.shortcuts import render_to_response, redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.template import RequestContext, Context, loader
from django.forms import modelformset_factory
#from django import forms
import logging
from pprint import pprint

import codecs
import glob
from django.contrib import messages
from django.contrib.messages import get_messages
import io
from django.core.files import File
import os
import shutil
import json
import decimal
import datetime
import time

from django.core.files.storage import FileSystemStorage
from django.core import serializers
from .models import Visiteur
from .forms import VisiteurForm
#import PIL
from PIL import Image, ImageOps
import datetime

from urllib.request import Request, urlopen
import requests
import re

static = '/home/dcallebaut/apps/vcastatic/'
canon = 'https://vincent.callebaut.org/'
global modif
modif = "no"


def video__player(request, lien="1SVCbWFtn3s", untitreesp='danieldefaut'):
    form = VisiteurForm()
    titre_espace = untitreesp.replace('_', ' ')
    titre_espace = titre_espace.lstrip()
    #titre_espace = _imgalt(request,'videos',)
    tup = listlast(request)

    args = {"lien": lien}
    args['form'] = form
    args['tup'] = tup
    args['meta_titre'] = titre_espace
    return render(request, 'video__player.html', args)


def vigvideo(request, categorie, date_projet):

    if request.method == "POST":
        projet = date_projet[7:]
        racine = static + 'videos/'

        files = request.FILES.getlist('myfiles')
        dossier = request.POST.get('dossier')

        image = Image.open(files[0])
        w, h = image.size
        ratio = w/float(h)

        new_height_thumb = int(720/float(ratio))
        new_height_full = int(1800/float(ratio))
        imgthumb = image.resize((720, new_height_thumb), Image.ANTIALIAS)
        #imgthumb_crop = imgthumb.crop((0,0,720,509))
        bord = new_height_thumb-float(390)
        marge_haute = 0
        if bord > 0:
            marge_haute = int(bord/float(2))
        imgthumb_crop = imgthumb.crop((0, marge_haute, 720, marge_haute+390))
        imgthumb_crop.save(racine+str(dossier)+'/thumb/' +
                           str(dossier)+'.jpg', 'JPEG', quality=30)
        imgfull = image.resize((1800, new_height_full), Image.ANTIALIAS)
        imgfull.save(racine+str(dossier)+'/hr/' +
                     str(dossier)+'.jpg', 'JPEG', quality=30)

        return HttpResponseRedirect("//vincent.callebaut.org/category/videos/admin/")
        # return HttpResponse("<br><br><br><br><br><br><br><br><br><br><br>Vignette et images en place :"+str(files[0])+str(dossier) )

    # Not POST
    old_date = date_projet[:6]
    projet = date_projet[7:]
    return render(request, "upvigvideo.html", {'projet': date_projet})


def listlast(request):
    racine = static + '/projects/'
    lislast = os.listdir(racine)
    lislast.sort(reverse=True)
    # selectionne les 6 derniers projets
    lislast = lislast[0:6]

    tup = []
    for img in lislast:
        imgs = os.listdir(racine+img+'/thumb/')
        imgs.sort()
        single = imgs[0:1]
        lien = img[7:]
        tup.append(img)
        tup.append(single[0])
        tup.append(lien)
    return (tup)


def _ip_visiteur(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _lacook(request):
    try:
        cook = request.COOKIES['modif']
    except:
        cook = "no"
    return cook


def sauve_visiteur(request):
    ip = _ip_visiteur(request)
    if request.POST:
        form = VisiteurForm(request.POST or None)
        if form.is_valid():
            mail = request.POST.get("email")
            testMail = Visiteur(email=mail, ip=ip, test=dh(request))
            testMail.save()
            #select =  User.objects.filter(email='daniel@callebaut.org')
            # if select > 0:
            request.session['logged_email'] = mail
            return HttpResponseRedirect('/merci/')
            # return render(request,'merci.html', {"cook": mail})
            # else


def dh(request):
    return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def index(request):
    ip = _ip_visiteur(request)
    cook = _lacook(request)
    form = VisiteurForm()
    envisite = Visiteur(page='index', ip=ip, test=dh(request))
    envisite.save()

    dossier_projets = static + "/projects/"
    liste_projets = os.listdir(dossier_projets)
    liste_projets.sort(reverse=True)
    projet_dir = []
    ii = 0
    exclu = ['101021_greenwave', '060416_jeongok', '060114_estonie', '050925_geneve', '050116_san_francisco', '041201_floatingislands', '040731_maurice',
             '040730_mauritius', '031130_tubize', '031030_edf', '030930_dublin', '030930_busan', '011201_elasticity', '011030_saint_etienne', '010830_quai_branly', '010401_canal']

    for projet in liste_projets:
        if projet not in exclu:

            list_images = os.listdir(dossier_projets+projet+'/hr/')
            list_images.sort()
            # 1° image
            image = list_images[0]
            first_slide = image
            # ajoute la planche 000
            phrase_thumb = 'projects/'+projet+'/thumb/'+image

            phrase_hr = 'projects/'+projet+'/hr/'+image
            img_alt = _imgalt(request, 'projects', projet,)
            projet_dir.append([phrase_thumb, phrase_hr, img_alt])

    args = {"meta_titre": 'VINCENT CALLEBAUT ARCHITECTURES PARIS'}

    #args['form'] = form
    args['liste_thumb'] = projet_dir
    args['firstslide'] = first_slide,
    tup = listlast(request)
    args['tup'] = tup
    args['form'] = form
    args['meta_desc'] = "Awarded in the top 50 of the Green Planet Architects, Vincent Callebaut Architectures is referenced as the best eco-prospective and visionary architectural"
    args['canonical'] = "https://vincent.callebaut.org/"
    args['cook'] = cook
    return render(request, 'index.html', args)


def cv(request, mode='user'):
    ip = _ip_visiteur(request)
    cook = _lacook(request)
    form = VisiteurForm()
    envisite = Visiteur(page='cv', ip=ip, test=dh(request))
    envisite.save()

    objet = ""
    lien = "cv_txt_us_desc_us"
    # titrecv1 =  open(static + "cv/txt/us/titre_us.txt")
    # cvrl = cv1.readlines()
    # titrecv = titrecv1.readlines()
    # for i in range(9):
    #     objet = objet + str(cv1.readline())+'<br>'

    title = "PROFILE"
    args = {"titrecv": 'titrecv'}
    args['form'] = form

    #args['mode']= mode
    args['lien'] = lien
    args['meta_titre'] = title
    args['meta_desc'] = title
    args['menu'] = 'Profile'
    tup = listlast(request)
    args['tup'] = tup
    args['cook'] = cook

    return render(request, 'cv.html', args)


def category(request, categorie='projects', mode=None):

    racine = static + categorie + "/"
    dossier_projets = static + categorie + "/"
    liste_projets = os.listdir(dossier_projets)
    liste_projets.sort(reverse=True)
    item_list = []
    cpt = 0
    for date_projet in liste_projets:
        # on recherche les images dns dossier hr
        cpt = cpt+1

        liste_images = os.listdir(dossier_projets+"/"+date_projet+'/hr/')
        liste_images.sort(reverse=False)
        try:
            vignette = liste_images[0]
            title_href = vignette[:-4]
        except:
            vignette = 'pbvig'
            title_href = ""
        projet = date_projet[7:len(date_projet)]  # on enleve la date du debut
        titre = ['pas de titre']
        untitre = ""
        try:
            #tit = os.listdir(racine+date_projet+"/txt/us/")
            # if 'tit' in tit[0]:
            #titrer = codecs.open(racine+date_projet+"/txt/us/"+tit[0], "r")
            titrer = codecs.open(racine+date_projet +
                                 "/txt/us/titre_us.txt", "r")
            untitre = titrer.readline()
            titre = titrer.readlines()
        except:
            titre = ['pas de titre']
            untitre = ""
            pass

        try:
            fic_lien = codecs.open(racine+date_projet+"/txt/us/lien.txt", "r")
            lien = fic_lien.readline()
        except:
            lien = date_projet

        untitreesp = "VCA"
        try:
            untitreesp = untitre.replace(',', ' ')
            untitreesp = untitreesp.replace(' ', '_')
        except:
            pass
        proj_titre = [date_projet]
        proj_titre.append(projet)
        proj_titre.append(vignette)
        proj_titre.append(untitre)
        proj_titre.append(titre)
        proj_titre.append(lien)
        proj_titre.append(title_href)
        proj_titre.append(untitreesp)
        item_list.append(proj_titre)
    if categorie == 'projects':
        meta_desc = "All projects Vincent Callebaut Architectures Paris"
        menu = 'Projects'
        description = "Vincent Callebaut Architectures, Sustainable Architecture, Biomimicry Design, Paris Smart City 2050, Lilypad, Dragonfly, Tao Zhu Yin Yuan, Agora Garden"
        canonical = canon+'category/projects'
    if categorie == 'videos':
        menu = 'Videos'
        title = "All Vidéos"
        meta_desc = "All Videos Vincent Callebaut Architectures Paris"
        description = "Vincent Callebaut Architectures, Talks, TEDx, TV Interviews, TF1, France 2, Arte, M6, LCP, City of Future, Sustainability, Energy Plus, Circular Economy"
        canonical = canon+"category/videos"
    if categorie == 'exhibitions':
        meta_desc = "All exhibitions Vincent Callebaut Architectures Paris"
        menu = 'Exhibitions'
        description = "Vincent Callebaut Architectures, Exhibitions, Conferences, Lectures, International Architecture, Innovation Awards, Architecture Biennial, World Exhibition"
        canonical = canon+"category/exhibitions"
    if categorie == 'publications':
        meta_desc = "All publications Vincent Callebaut Architectures Paris"
        menu = 'Publications'
        description = "Vincent Callebaut Architectures, Press Releases, Monographies, Books, Paris 2050, Fertile Cities, Archibiotic, Interviews, CNN, BBC, Time, Green Building"
        canonical = canon+"category/publications"

    title = categorie.capitalize()   # aussi utilisé our video

    args = {"untitreesp": ''}
    args['description'] = description
    args['item_list'] = item_list
    args['categorie'] = categorie
    args['mode'] = mode
    args['form'] = form
    args['title'] = title
    args['menu'] = menu
    args['meta_desc'] = meta_desc
    args['canonical'] = canonical
    args['vignette'] = "vignette"
    tup = listlast(request)
    args['tup'] = tup
    args['cook'] = cook
    # TODO: test 'category.html'
    return render(request, 'videos.html', args)


def contact(request, mode='user'):
    ip = _ip_visiteur(request)
    cook = _lacook(request)
    form = VisiteurForm()
    envisite = Visiteur(page='contact', ip=ip, test=dh(request))
    envisite.save()
    titrecont1 = open(static + 'contact/txt/us/titre_us.txt')
    titrecont = titrecont1.readlines()
    tup = listlast(request)
    title = "CONTACT"
    args = {"menu": "Contact"}
    args['titrecont'] = titrecont
    args['range'] = range(10)
    args['mode'] = mode
    args['title'] = 'title'
    args['form'] = form
    args['meta_titre'] = title
    args['meta_desc'] = 'Contact Vincent Callebaut Architectures Paris'
    args['tup'] = tup
    args['cook'] = cook
    # args['tup']=tup
    return render(request, 'contact.html', args)


def myadmin(request):
    try:
        cook = request.COOKIES['modif']
    except:
        cook = "no"

    visiteurs = Visiteur.objects.all().order_by(
        '-test')  # Nous sélectionnons tous nos articles
    cpt = Visiteur.objects.all().count()
    form = VisiteurForm()
    args = {"cpt": cpt}
    args['form'] = form
    args['visiteurs'] = visiteurs
    tup = listlast(request)
    args["cook"] = cook
    args["cpt"] = cpt
    args['tup'] = tup
    return render(request, 'myadmin.html', args)


def myhelp(request):
    try:
        cook = request.COOKIES['modif']
    except:
        cook = "no"
    tup = listlast(request)
    args = {"cook": cook}
    args['tup'] = tup
    return render(request, 'myhelp.html', args)


def projet(request, date_projet='x', projet='aequorea', categorie="projects", mode=''):

    ip = _ip_visiteur(request)
    cook = _lacook(request)
    form = VisiteurForm()
    envisite = Visiteur(page=projet, ip=ip, test=dh(request))
    envisite.save()

    erreur = ''
    first_slide = ""
    #racine ="/home/dcalleba/webapps/vincent_static/static/vca/images/vincent/"
    racine = static
    dossier = categorie+"/"+date_projet+"/"

    #urlcan = "http://vincent.callebaut.org/object/"+date_projet+"/"+projet+"/"+categorie
    image = projet
    qtyfile = len(os.listdir(racine+dossier))-4
    img_alt = _imgalt(request, categorie, date_projet)
    og_url = "https://vincent.callebaut.org"+request.get_full_path()

    # try:
    #     titrer = codecs.open(racine+dossier+"txt/us/titre_us.txt", "r")
    #     untitre = titrer.readline()
    #     untitre = untitre.decode("utf-8")
    #     untitre = unicode(untitre)
    #     untitre = untitre.encode("ascii","ignore")
    #     untitre = untitre.lstrip()
    # except:
    #     pass
    # try:
    #     titrer2 = codecs.open(racine+dossier+"txt/us/titre_us.txt", "r")
    #     grand_titre = titrer2.readlines()
    #     meta_desc = ""
    #     grand_titres = ""
    #     for lig in grand_titre:
    #         meta_desc = meta_desc+ lig
    #         lig = lig.decode("utf-8")
    #         lig = unicode(lig)
    #         lig = lig.encode("ascii","ignore")

    #         grand_titres =grand_titres + lig
    #     grand_titres = grand_titres.lstrip()
    # except:
    #     grand_titre = ["Grand Titre"]
    #     untitre = u"unknow"

    try:
        meta_titre = _metatitle(request, categorie, date_projet)
        desc = ''
    except:
        # TODO:revoir si pas de metadesc
        meta_titre = "PROJECT : - Vincent Callebaut Architectures Paris"
        desc = "No "

    try:
        meta_desc = _metadesc(request, categorie, date_projet)
        desc = ''
    except:
        # TODO:revoir si pas de metadesc
        meta_desc = "PROJECT : - Vincent Callebaut Architectures Paris"
        desc = "No "
    # Fiche  -----------------------------------------------------------
    try:
        fichier = codecs.open(racine+dossier+"txt/us/fiche_us.txt", "r")
        envoi = []
        fich = fichier.readlines()
        for lig in fich:
            ' '.join(lig.split())
            if len(lig) > 1:
                # lig.replace("<br>","")
                envoi.append(lig)
        fiche = envoi
    except:
        fiche = ["Il n'existe pas de fiche"]

    item_list = []
    data_slide = []
    filenames = []
    liste_images = os.listdir(static+categorie+"/"+date_projet+"/hr/")
    liste_images.sort()
    cpt = 0
    for image in liste_images:
        if image > '':
            img_alt = _imgalt(request, categorie, date_projet)
            image = image.lower()
            (filepath, filename) = os.path.split(image)
            cpt = cpt+1
            # au cas ou il n'y en aurait pas
            second_slide = static+categorie+"/"+date_projet+"/hr/"+filename
            # memorise les 2 premières images en vue utilisation facebook og
            if cpt == 1:
                first_slide = static+categorie+"/"+date_projet+"/hr/"+filename
            if cpt == 2:
                second_slide = static+categorie+"/"+date_projet+"/hr/"+filename
            if cpt == 1:
                og_image = "https://vincent.callebaut.org/static/" + \
                    categorie+"/"+date_projet+"/thumb/"+filename
            # if cpt >20 :
            #    break
            imghr = '/static/'+categorie+"/"+date_projet+"/hr/"+filename
            #imgthumb =  "http://static.callebaut.org/static/vca/images/vincent/"+categorie+"/"+date_projet+"/thumb/"+filename
            #imgthumbnew = '/static/'+categorie+"/"+date_projet+"/thumb/"+filename
            imgthumb = filename
            # item_list.append(imghr)   # toutes les vignettes pour grille après fiche
            # data_slide.append(imgthumb)
            # if categorie == "projects":
            if categorie in ["publications", "projects", "exhibitions"]:

                if imgthumb[-9:] != "pl000.jpg":  # correction ce 30/11/2020
                    imgthumb = imgthumb.replace(".jpg", "")
                    data_slide.append([imgthumb, img_alt])

                if imghr[-9:] != "pl000.jpg":
                    item_list.append([imghr, img_alt])
                filenames.append(filename)

            # if categorie not in  ["publications","exhibitions"]:
            else:
                data_slide.append(imgthumb)
                if cpt == 1:
                    # si il n'y a qu'une image
                    item_list.append(imghr)
                if cpt >= 2:
                    try:
                        filenames.append(filename)
                        item_list.append(imghr)
                        # data_slide.append(imgthumb)
                    except:
                        erreur = "pas de append"

    filenames.sort()
    item_list.sort()
    data_slide.sort()
    #erreur = data_slide[0]

    cattitre = ""  # +categorie[:4].lower()

    titre_title = _imgalt(request, categorie, date_projet)

    #untitre = untitre.lstrip()[0:27]
    untitre = titre_title
    untitre = untitre[:65]

    ca = " "
    # TODO: rvoir grand titre de txt à html
    try:
        grand_titres = grand_titres.lstrip()[:103]
    except:
        pass
    if categorie == "projects":
        ca = "Project"
        menu = "Projects"
    if categorie == "exhibitions":
        ca = "Exhibition"
        menu = "Exhibitions"
        # Fichemeta_desc = "EXIBITIONS : "+ grand_titres + " Vincent Callebaut Architectures Paris"
        #meta_desc = "EXIBITIONS :  Vincent Callebaut Architectures Paris"
    if categorie == "publications":
        ca = "Publication"
        menu = "Publications"
        #meta_desc = "PUBLICATION : "+ grand_titres + " Vincent Callebaut Architectures Paris"
        #meta_desc = "PUBLICATION :  Vincent Callebaut Architectures Paris"
    if categorie == "videos":
        #untitre = 'VCA'
        ca = "Video"
        menu = "Videos"
        #meta_desc = "VIDEOS : "+ grand_titres + " Vincent Callebaut Architectures Paris."
        #meta_desc = "VIDEOS :  Vincent Callebaut Architectures Paris."

    tup = listlast(request)
    if cpt < 5:
        vigdef = 'full'
    else:
        vigdef = 'min'

    args = {'menu': menu}
    args['form'] = form
    args['categorie'] = categorie
    args['valeurs'] = 'dan'
    args['item_list'] = item_list
    args['data_slide'] = data_slide
    args['liste_projets'] = data_slide
    args['first_slide'] = first_slide
    args['second_slide'] = second_slide
    #args['urlcan']=  urlcan
    args['dossier'] = projet.upper()
    args['date_projet'] = date_projet
    #args['grand_titre']=  grand_titre
    args['desc'] = desc

    args['mode'] = mode
    #args['title']= untitre

    args['filenames'] = filenames
    args['projet'] = projet
    args['vignette'] = erreur

    args['tup'] = tup
    args['liste_images'] = liste_images
    args['desc_lien'] = categorie+"/"+date_projet+"/txt/us/desc_us.html"
    args['fiche_lien'] = categorie+"/"+date_projet+"/txt/us/fiche_us.html"
    args['titre_lien'] = categorie+"/"+date_projet+"/txt/us/titre_us.html"
    args['cook'] = cook
    args['filename'] = filename
    args['vigdef'] = vigdef

    args['meta_titre'] = meta_titre
    args['meta_desc'] = meta_desc
    args['img_alt'] = img_alt
    args['og_image'] = og_image
    args['og_url'] = og_url

    #args['img_alt'] = img_alt
    #args['canonical']= urlcan
    return render(request, 'projet.html', args)


def projects(request, categorie='projects', mode=None):
    ip = _ip_visiteur(request)
    cook = _lacook(request)
    form = VisiteurForm()
    envisite = Visiteur(page='projets', ip=ip, test=dh(request))
    envisite.save()
    racine = static + categorie+"/"
    dossier_projets = static + categorie + "/"
    try:
        cook = request.COOKIES['modif']
    except:
        cook = "no"

    liste_projets = os.listdir(dossier_projets)
    liste_projets.sort(reverse=True)
    item_list = []
    cpt = 0
    for date_projet in liste_projets:
        img_alt = _imgalt(request, categorie, date_projet)
        # try:
        #     #titre google pour alt img lit d'un fichier txt qui n'est plus créé
        #     lefichier = static+categorie+"/"+date_projet+"/txt/us/titre_us.txt"
        #     with open(lefichier, "r") as file:
        #         img_alt = file.readline()
        # except:
        #     img_alt= date_projet#"- Vincent Callebaut Architectures -"

        # on recherche les images dns dossier hr
        cpt = cpt+1
        liste_images = os.listdir(dossier_projets+date_projet+'/hr/')
        liste_images.sort(reverse=False)
        try:
            vignette = liste_images[0]
            title_href = vignette[:-4]
        except:
            vignette = 'pbvig'
            title_href = ""
        projet = date_projet[7:len(date_projet)]  # on enleve la date du debut
        titre = ['pas de titre']

        try:
            # titre sous vignette
            titre_lien = categorie+"/"+date_projet+"/txt/us/titre_us.html"
        except:
            titre_lien = "erreur2.html"

        try:
            fic_lien = codecs.open(racine+date_projet+"/txt/us/lien.txt", "r")
            lien = fic_lien.readline()
        except:
            lien = date_projet
        vignette_desc = ""
        untitreesp = "VCA"

        proj_titre = [date_projet]
        proj_titre.append(projet)
        proj_titre.append(vignette)
        proj_titre.append(titre_lien)
        proj_titre.append(vignette_desc)
        proj_titre.append(titre)
        proj_titre.append(lien)
        proj_titre.append(title_href)
        proj_titre.append(untitreesp)
        proj_titre.append(cook)
        proj_titre.append(img_alt)

        item_list.append(proj_titre)
    if categorie == 'projects':
        meta_desc = "All projects Vincent Callebaut Architectures Paris"
        menu = 'Projects'
        description = "Vincent Callebaut Architectures, Sustainable Architecture, Biomimicry Design, Paris Smart City 2050, Lilypad, Dragonfly, Tao Zhu Yin Yuan, Agora Garden"
        canonical = canon+'category/projects'
    if categorie == 'videos':
        menu = 'Videos'
        title = "All Vidéos"
        meta_desc = "All Videos Vincent Callebaut Architectures Paris"
        description = "Vincent Callebaut Architectures, Talks, TEDx, TV Interviews, TF1, France 2, Arte, M6, LCP, City of Future, Sustainability, Energy Plus, Circular Economy"
        canonical = canon+"category/videos"
    if categorie == 'exhibitions':
        meta_desc = "All exhibitions Vincent Callebaut Architectures Paris"
        menu = 'Exhibitions'
        description = "Vincent Callebaut Architectures, Exhibitions, Conferences, Lectures, International Architecture, Innovation Awards, Architecture Biennial, World Exhibition"
        canonical = canon+"category/exhibitions"
    if categorie == 'publications':
        meta_desc = "All publications Vincent Callebaut Architectures Paris"
        menu = 'Publications'
        description = "Vincent Callebaut Architectures, Press Releases, Monographies, Books, Paris 2050, Fertile Cities, Archibiotic, Interviews, CNN, BBC, Time, Green Building"
        canonical = canon+"category/publications"

    title = categorie.capitalize()   # aussi utilisé our video

    args = {"untitreesp": ''}
    args['description'] = description
    args['item_list'] = item_list
    args['categorie'] = categorie
    args['mode'] = mode
    args['form'] = form

    #args['vignette_desc']= 'Daniel vignette_desc'

    args['title'] = title
    args['menu'] = menu
    args['meta_titre'] = "PROJECTS"
    args['meta_desc'] = meta_desc
    #args['canonical']= canonical
    args['vignette'] = "vignette"

    tup = listlast(request)
    args['tup'] = tup
    args['cook'] = cook

    return render(request, 'projects.html', args)


def publications(request, categorie='publications', mode=None):
    ip = _ip_visiteur(request)
    cook = _lacook(request)
    form = VisiteurForm()
    envisite = Visiteur(page='pulications', ip=ip, test=dh(request))
    envisite.save()

    modif = request.COOKIES.get('modif')

    racine = static + categorie+"/"
    dossier_projets = static + categorie + "/"
    liste_projets = os.listdir(dossier_projets)
    liste_projets.sort(reverse=True)
    item_list = []
    cpt = 0
    for date_projet in liste_projets:
        img_alt = _imgalt(request, categorie, date_projet)
        dossier = categorie+"/"+date_projet+"/"
        #desc_txt  = htmltxt(request,dossier)
        meta_desc = _metadesc(request, categorie, date_projet)
        desc_txt = meta_desc
        desc = ''

        # on recherche les images dns dossier hr
        cpt = cpt+1

        liste_images = os.listdir(dossier_projets+"/"+date_projet+'/hr/')
        liste_images.sort(reverse=False)
        try:
            vignette = liste_images[0]
            title_href = vignette[:-4]
        except:
            vignette = 'pbvig'
            title_href = ""
        projet = date_projet[7:len(date_projet)]  # on enleve la date du debut
        titre = ['pas de titre']
        untitre = ""
        try:
            #tit = os.listdir(racine+date_projet+"/txt/us/")
            # if 'tit' in tit[0]:
            #titrer = codecs.open(racine+date_projet+"/txt/us/"+tit[0], "r")
            titrer = codecs.open(racine+date_projet +
                                 "/txt/us/titre_us.txt", "r")
            untitre = titrer.readline()
            titre = titrer.readlines()
        except:
            titre = ['pas de titre']
            untitre = ""
            pass
        try:
            # titre sous vignette
            titre_lien = categorie+"/"+date_projet+"/txt/us/titre_us.html"
        except:
            titre_lien = "erreur2.html"

        try:
            fic_lien = codecs.open(racine+date_projet+"/txt/us/lien.txt", "r")
            lien = fic_lien.readline()
        except:
            lien = date_projet

        untitreesp = "VCA"
        try:
            untitreesp = untitre.replace(',', ' ')
            untitreesp = untitreesp.replace(' ', '_')
        except:
            pass

        vignette_desc = ""

        proj_titre = [date_projet]
        proj_titre.append(projet)
        proj_titre.append(vignette)
        proj_titre.append(titre_lien)
        proj_titre.append(vignette_desc)
        proj_titre.append(titre)
        proj_titre.append(lien)
        proj_titre.append(title_href)
        proj_titre.append(untitreesp)
        proj_titre.append(cook)
        proj_titre.append(img_alt)
        proj_titre.append(meta_desc)
        item_list.append(proj_titre)
    if categorie == 'projects':
        #meta_desc = "All PUBLICATIONS Vincent Callebaut Architectures Paris"
        menu = 'Projects'
        description = "Vincent Callebaut Architectures, Sustainable Architecture, Biomimicry Design, Paris Smart City 2050, Lilypad, Dragonfly, Tao Zhu Yin Yuan, Agora Garden"
        canonical = canon+'category/projects'
    if categorie == 'videos':
        menu = 'Videos'
        title = "All Vidéos"
        #meta_desc = "All Videos Vincent Callebaut Architectures Paris"
        description = "Vincent Callebaut Architectures, Talks, TEDx, TV Interviews, TF1, France 2, Arte, M6, LCP, City of Future, Sustainability, Energy Plus, Circular Economy"
        canonical = canon+"category/videos"
    if categorie == 'exhibitions':
        #meta_desc = "All exhibitions Vincent Callebaut Architectures Paris"
        menu = 'Exhibitions'
        description = "Vincent Callebaut Architectures, Exhibitions, Conferences, Lectures, International Architecture, Innovation Awards, Architecture Biennial, World Exhibition"
        canonical = canon+"category/exhibitions"
    if categorie == 'publications':
        #meta_desc = "All publications Vincent Callebaut Architectures Paris,-"
        menu = 'Publications'
        description = "Vincent Callebaut Architectures, Press Releases, Monographies, Books, Paris 2050, Fertile Cities, Archibiotic, Interviews, CNN, BBC, Time, Green Building"
        canonical = canon+"category/publications"

    title = categorie.capitalize()   # aussi utilisé our video
    if cpt < 5:
        vigdef = 'min'
    else:
        vigdef = 'full'
    args = {"untitreesp": ''}
    args['description'] = description
    args['item_list'] = item_list
    args['categorie'] = categorie
    args['mode'] = mode
    args['form'] = form
    args['title'] = title
    args['menu'] = menu
    args['meta_titre'] = "PUBLICATIONS"
    args['meta_desc'] = meta_desc
    #args['canonical']= canonical
    args['vignette'] = "vignette"
    args['titre_lien'] = titre_lien
    tup = listlast(request)
    args['tup'] = tup
    args['cook'] = cook
    args['vigdef'] = vigdef

    return render(request, 'publications.html', args)


def exhibitions(request, categorie='exhibitions', mode=None):
    ip = _ip_visiteur(request)
    cook = _lacook(request)
    form = VisiteurForm()
    envisite = Visiteur(page='exhibitions', ip=ip, test=dh(request))
    envisite.save()

    racine = static + categorie+"/"
    dossier_projets = static + categorie + "/"
    liste_projets = os.listdir(dossier_projets)
    liste_projets.sort(reverse=True)
    item_list = []
    cpt = 0
    for date_projet in liste_projets:
        img_alt = _imgalt(request, categorie, date_projet)
        dossier = categorie+"/"+date_projet+"/"
        desc_txt = htmltxt(request, dossier)
        meta_desc = _metadesc(request, categorie, date_projet)
        desc = ''

        # on recherche les images dns dossier hr
        cpt = cpt+1

        liste_images = os.listdir(dossier_projets+"/"+date_projet+'/hr/')
        liste_images.sort(reverse=False)
        try:
            vignette = liste_images[0]
            title_href = vignette[:-4]
        except:
            vignette = 'pbvig'
            title_href = ""
        projet = date_projet[7:len(date_projet)]  # on enleve la date du debut
        titre = ['pas de titre']
        untitre = ""
        try:
            # titre sous vignette
            titre_lien = categorie+"/"+date_projet+"/txt/us/titre_us.html"
        except:
            titre_lien = "erreur2.html"

        try:
            fic_lien = codecs.open(racine+date_projet+"/txt/us/lien.txt", "r")
            lien = fic_lien.readline()
        except:
            lien = date_projet

        untitreesp = "VCA"
        try:
            untitreesp = untitre.replace(',', ' ')
            untitreesp = untitreesp.replace(' ', '_')
        except:
            pass

        vignette_desc = ''

        proj_titre = [date_projet]
        proj_titre.append(projet)
        proj_titre.append(vignette)
        proj_titre.append(titre_lien)
        proj_titre.append(vignette_desc)
        proj_titre.append(titre)
        proj_titre.append(lien)
        proj_titre.append(title_href)
        proj_titre.append(untitreesp)
        proj_titre.append(cook)
        proj_titre.append(img_alt)
        proj_titre.append(meta_desc)
        item_list.append(proj_titre)

    if categorie == 'exhibitions':
        meta_desc = "All exhibitions Vincent Callebaut Architectures Paris"
        menu = 'Exhibitions'
        description = "Vincent Callebaut Architectures, Exhibitions, Conferences, Lectures, International Architecture, Innovation Awards, Architecture Biennial, World Exhibition"
        canonical = canon+"category/exhibitions"

    args = {"untitreesp": ''}
    args['description'] = description
    args['item_list'] = item_list
    args['categorie'] = categorie
    args['mode'] = mode
    args['form'] = form
    #args['title']= title
    args['menu'] = menu
    args['meta_titre'] = "EXHIBITIONS"
    args['meta_desc'] = meta_desc
    #args['canonical']= canonical
    args['vignette'] = "vignette"
    tup = listlast(request)
    args['tup'] = tup
    args['cook'] = cook

    return render(request, 'exhibitions.html', args)


def setAdminOn(request):
    response = HttpResponseRedirect('/')
    response.set_cookie('modif', 'ok', max_age=14400)
    return response


def setAdminOff(request):
    response = HttpResponseRedirect('/')
    response.set_cookie('modif', 'no', max_age=86400)
    return response


def vcaadmin(request, var):
    if var == "Roquette,2":
        args = {"tup": listlast(request)}
        args['form'] = VisiteurForm()
        return render(request, 'vcaadmin.html', args)
    else:
        response = HttpResponse(
            'Modifications ne sont plus autorisées <br> <a href="https://vincent.callebaut.org">Cliquer ici pour désactiver  Edition sur tout le site</a>')
        response.set_cookie('modif', 'no', max_age=86400)
        return response


def _imgalt(request, categorie, date_projet):
    try:
        r = requests.get("https://vincent.callebaut.org/static/" +
                         categorie+"/"+date_projet+"/txt/us/titre_us.html")
        r.encoding = ('UTF-8')
        texte = r.text
        pos1 = texte.find("</h3>")
        texte = texte[:pos1]
        texte = re.sub('<[^<]+?>', '', texte)
        img_alt = texte.strip()
    except:
        img_alt = date_projet  # "- Vincent Callebaut Architectures -"
    return img_alt


def _imgalttxt(request, categorie, date_projet):
    try:
        file = open("https://vincent.callebaut.org/static/" +
                    categorie+"/"+date_projet+"/txt/us/titlenew.txt", "r")
        texte = file.readline()
        img_alt = texte
    except:
        img_alt = date_projet  # "- Vincent Callebaut Architectures -"
    return img_alt


def videos(request, categorie='videos', mode=None):
    ip = _ip_visiteur(request)
    cook = _lacook(request)
    form = VisiteurForm()
    envisite = Visiteur(page='vidéos', ip=ip, test=dh(request))
    envisite.save()
    racine = static + categorie+"/"
    dossier_projets = static + categorie + "/"
    liste_projets = os.listdir(dossier_projets)
    liste_projets.sort(reverse=True)
    item_list = []
    cpt = 0
    for date_projet in liste_projets:
        img_alt = _imgalt(request, categorie, date_projet)
        # on recherche les images dns dossier hr
        cpt = cpt+1

        liste_images = os.listdir(dossier_projets+"/"+date_projet+'/hr/')
        liste_images.sort(reverse=False)
        try:
            vignette = liste_images[0]
            title_href = vignette[:-4]
        except:
            vignette = 'pbvig'
            title_href = ""
        projet = date_projet[7:len(date_projet)]  # on enleve la date du debut
        titre = ['pas de titre']
        untitre = ""

        try:
            # titre sous vignette
            titre_lien = categorie+"/"+date_projet+"/txt/us/titre_us.html"
        except:
            titre_lien = "erreur2.html"

        try:
            fic_lien = codecs.open(racine+date_projet+"/txt/us/lien.txt", "r")
            lien = fic_lien.readline()
        except:
            lien = date_projet

        untitreesp = "VCA"
        try:
            untitreesp = untitre.replace(',', ' ')
            untitreesp = untitreesp.replace(' ', '_')
        except:
            pass
        img_alt = img_alt.replace(" ", "_")
        img_alt = img_alt.replace(",", "_")
        img_alt = img_alt.replace("+", " ")
        img_alt = img_alt.replace("/", "_")
        img_alt = img_alt
        proj_titre = [date_projet]
        proj_titre.append(projet)
        proj_titre.append(vignette)
        proj_titre.append(titre_lien)
        proj_titre.append(titre)
        proj_titre.append(lien)
        proj_titre.append(title_href)
        proj_titre.append(untitreesp)
        proj_titre.append(img_alt)
        item_list.append(proj_titre)
    if categorie == 'projects':
        meta_desc = "All projects Vincent Callebaut Architectures Paris"
        menu = 'Projects'
        description = "Vincent Callebaut Architectures, Sustainable Architecture, Biomimicry Design, Paris Smart City 2050, Lilypad, Dragonfly, Tao Zhu Yin Yuan, Agora Garden"
        canonical = canon+'category/projects'
    if categorie == 'videos':
        menu = 'Videos'
        title = "All Vidéos"
        meta_desc = "All Videos Vincent Callebaut Architectures Paris"
        description = "Vincent Callebaut Architectures, Talks, TEDx, TV Interviews, TF1, France 2, Arte, M6, LCP, City of Future, Sustainability, Energy Plus, Circular Economy"
        canonical = canon+"category/videos"
    if categorie == 'exhibitions':
        meta_desc = "All exhibitions Vincent Callebaut Architectures Paris"
        menu = 'Exhibitions'
        description = "Vincent Callebaut Architectures, Exhibitions, Conferences, Lectures, International Architecture, Innovation Awards, Architecture Biennial, World Exhibition"
        canonical = canon+"category/exhibitions"
    if categorie == 'publications':
        meta_desc = "All publications Vincent Callebaut Architectures Paris"
        menu = 'Publications'
        description = "Vincent Callebaut Architectures, Press Releases, Monographies, Books, Paris 2050, Fertile Cities, Archibiotic, Interviews, CNN, BBC, Time, Green Building"
        canonical = canon+"category/publications"

    title = categorie.capitalize()   # aussi utilisé our video

    args = {"untitreesp": ''}
    args['description'] = description
    args['item_list'] = item_list
    args['categorie'] = categorie
    args['mode'] = mode
    args['titre_lien'] = categorie+"/"+date_projet+"/txt/us/titre_us.html"
    args['form'] = form
    args['title'] = title
    args['menu'] = menu
    args['meta_titre'] = "VIDEOS"
    args['meta_desc'] = meta_desc
    #args['canonical']= canonical
    args['vignette'] = "vignette"
    tup = listlast(request)
    args['tup'] = tup
    args['cook'] = cook

    return render(request, 'videos.html', args)


def zoom(request, categorie="projects", date_projet="150527_woodenorchids", thumb='test'):
    tup = listlast(request)
    form = VisiteurForm()
    image_lien = categorie+"/"+date_projet+"/hr/"+thumb

    menu = categorie.capitalize()
    meta_titre = _metatitle(request, categorie, date_projet)
    args = {"untitreesp": 'ddd'}
    args['tup'] = tup
    args['meta_titre'] = meta_titre  # 'zoom project Vincent Callebaut'
    args['categorie'] = categorie
    args['date_projet'] = date_projet
    args['thumb'] = thumb
    args['form'] = form

    return render(request, 'zoom.html', args)


def eff_proj(request, dossier, projet):
    racine = '/home/dcallebaut/apps/vcastatic/'
    try:
        if os.path.exists(racine+dossier+"/"+projet):
            shutil.rmtree(racine+dossier+"/"+projet)
            return HttpResponse("<br><br><br><br><br><br><br><br><br><br><br>Dossier supprimé avec succés <a href='https://vincent.callebaut.org/projects'>Cliquer ici pour retour au projets</a>")
        else:
            return HttpResponse(u"<br><br><br><br><br><br><br><br><br><br><br>Erreur : le dossier " + racine+dossier+"/"+projet+u" n'a pas pu être supprimé ")
    except:
        return HttpResponse(u"<br><br><br><br><br><br><br><br><br><br><br>Erreur : le dossier " + racine+dossier+"/"+projet+u" n'a pas pu être supprimé ")


def ren_proj(request, categorie, date_projet):
    if request.method == "POST":
        projet = date_projet[7:]
        racine = '/home/dcallebaut/apps/vcastatic/'+categorie+"/"
        data = request.POST.get('new_date')
        new_dossier = request.POST.get('new_dossier')
        os.rename(racine+date_projet, racine+data+"_"+new_dossier)
        return HttpResponseRedirect("//vincent.callebaut.org/category/"+categorie+"/admin")


def replace_str_index(text, index=0, replacement=''):
    return '%s%s%s' % (text[:index], replacement, text[index+1:])


def trumbo(request, lien="cv/txt/us/desc_us"):

    if lien == "cv":
        lien = static + "/cv/txt/us/desc_us.html"
        lien_min = "cv/txt/us/desc_us.html"
    elif lien == "about":
        lien = static + "/about/txt/us/desc_us.html"
        lien_min = "about/txt/us/desc_us.html"
    else:
        #request.session['ficmodif'] = lien

        file_slash = lien.replace("_", "/")
        # remplace la derniere occurence  ---  http://www.python-simple.com/python-langage/chaines-de-caracteres-string.php
        old = '/'
        new = '_'
        maxreplace = 1

        lien = new.join(file_slash.rsplit(old, maxreplace))+'.html'

        # _____________________________
        # eesaie de trouver un _ 2020_projetdeparis
        ind = lien.find('/', 14, 20)
        lien = replace_str_index(lien, ind, '_')
        # _____________________________

        lien_min = lien
        lien = static+lien
        # logging.warning('ok')
    with open(lien, "r") as fic:
        fictxt = fic.readlines()
        data = ''
        cpt = 0
        for lig in fictxt:
            lig = lig
            cpt = cpt+1
            if lig.__len__ == 0:
                lig = "<br>"
                logging.warning('ok')
            data = data+lig

    with io.open(lien, 'w', encoding='utf8') as f:
        myfile = File(f)
        myfile.write(data)
        myfile.closed
        f.closed
    #lien = static+"projects"+"/"+"200207_rainbowtree"+"/txt/us/desc_us.txt"
    request.session['recook'] = lien
    recook = request.session['recook']
    args = {"data": data}
    args['lien'] = lien
    args['recook'] = recook
    args['lien_min'] = lien_min
    #args['recook']= recook
    return render(request, 'trumbo.html', args)


def filesave(request, lien="", data="Daniel callebaut"):
    datas = request.POST.get('obj')

    # lien = static+"cv/txt/us/desc_us.html"
    # with io.open(lien, 'w',encoding='utf8') as f:
    #     myfile = File(f)
    #     myfile.write(data)
    # myfile.closed
    # f.closed
    # args = {"data" : "vfvvfvd callebaut ficsend"}
    # return render(request,datas)
    return HttpResponse(datas)


def handle_uploaded_file(f):
    with open('name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def storage(request, file_name, myfile):
    return HttpResponse("probleme de sauvegarde du fichier :" + file_name)
    try:
        os.remove(static + file_name)
        # upload le fichier
        fs = FileSystemStorage(static)
        # myfile.name garde le nom d'origine
        filename = fs.save(file_name, myfile)
        #uploaded_file_url = fs.url('daniel')
    except:
        return HttpResponse("probleme de sauvegarde du fichier :"+file_name)
    return


def upload(request, kiwcom):

    recook = request.session['recook']
    try:
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']

            # return HttpResponse('hello'+myfile.name)
            if 'about' in myfile.name:
                file_name = "about/txt/us/desc_us.html"
                lien_min = "abou/txt/us/desc_us.html"
                # supprimer le fichier avant de le remplacer
                os.remove(static + file_name)
                # upload le fichier
                fs = FileSystemStorage(static)
                # myfile.name garde le nom d'origine
                filename = fs.save(file_name, myfile)
                return HttpResponseRedirect('https://vincent.callebaut.org')

            elif "cv" in myfile.name:
                # return HttpResponse("probleme de sauvegarde du fichier :"+myfile.name)
                file_name = "cv/txt/us/desc_us.html"
                lien_min = "cv/txt/us/desc_us.html"
                # supprimer le fichier avant de le remplacer
                os.remove(static + file_name)
                # upload le fichier
                fs = FileSystemStorage(static)  # static = dossier racine
                # myfile.name garde le nom d'origine
                filename = fs.save(file_name, myfile)
                return HttpResponseRedirect('https://vincent.callebaut.org/cv')
            else:
                # pour projet, publication, exhibition
                # reconstruit le repertoire
                file_slash = myfile.name.replace("_", "/")
                # remplace la derniere occurence
                old = '/'
                new = '_'
                maxreplace = 1
                file_final = new.join(file_slash.rsplit(old, maxreplace))
                file_lien = file_final
                # _____________________________
                # eesaie de trouver un _ 2020_projetdeparis #TODO:revoir séparateur 2020_projet
                ind = file_final.find('/', 14, 20)
                file_final = replace_str_index(file_final, ind, '_')
                # _____________________________
                # supprime la version duchier par ex xxx (2).html
                ind = 0
                ind = file_final.find("(")
                if ind > 0:
                    ind = ind-1
                    file_final = file_final[0:ind]+".html"
                # _____________________________
                # supprimer le fichier avant de le remplacer
                try:
                    os.remove(static + file_final)
                    # upload le fichier
                    fs = FileSystemStorage(static)
                    # myfile.name garde le nom d'origine
                    filename = fs.save(file_final, myfile)
                    #uploaded_file_url = fs.url('daniel')
                    # return HttpResponse(static +" : "+ file_final+" : "+ str(myfile))
                except:
                    return HttpResponse("probleme de sauvegarde d'un fichier projet-exhibitions-publications")

                # _____________________________
                # fabrique le lien de retour par ex : https://vincent.callebaut.fr/object/200207_rainbowtree/rainbowtree/projects
                # trouve la categorie
                ind = file_final.find("/")
                categorie = file_final[0:ind]
                file_final = file_final.replace(categorie, "")
                # enleve le 1°/
                file_final = (file_final[1:])
                ind = file_final.find("/")
                projet_date = str(file_final[0:ind])
                ind = projet_date.find("_")
                projet = (projet_date[ind+1:])
                #pprint (projet_date)
                return HttpResponseRedirect('https://vincent.callebaut.org/'+categorie)
                # return HttpResponseRedirect('https://vincent.callebaut.fr/object/'+projet_date+"/"+projet+"/"+categorie)
    except:
        return HttpResponse("<br>Ne pas oublier de selectionner le fichier !")

    # TODO: Lien sortie de upload par ex https://vincent.callebaut.fr/object/200207_rainbowtree/rainbowtree/projects
    args = {"recook": recook}
    #args['recook']= recook
    return render(request, 'upload.html', args)


def footer__email(request):
    if request.POST:
        form = VisiteurForm(request.POST or None)
        if form.is_valid():
            mail = request.POST.get("email")
            testMail = Visiteur(email=mail, ip=ip, test=dh(request))
            testMail.save()
            #select =  User.objects.filter(email='daniel@callebaut.org')
            # if select > 0:
            # request.session['logged_email']=mail
            return HttpResponseRedirect('/merci/')
    else:
        form = VisiteurForm()


def textareasub(request):
    args = {"recook": "recook"}
    #args['recook']= recook
    message = "Tout va bien"
    messages = "Tout va très bien"
    args = {"messages": messages}
    args['message'] = message
    return render(request, 'textareasub.html', args)


def creation(request, cat="defaut", date_projet="defaut", proj="def"):
    ladate = date_projet[:6]
    leprojet = date_projet[7:]
    globa = ""
    racine = '/home/dcallebaut/apps/vcastatic/'
    dos = racine+cat+"/"+date_projet+"/hr/"
    do = racine+cat+"/"+date_projet+"/"

    #allimg = []
    #images = os.listdir(dos)
    # for img in images:
    #    allimg.append(dos+img)

    if request.method == "POST":
        # recupere les valeurs de la form
        #files = allimg
        # if request.FILES.getlist('myfiles')[0] >"":
        files = request.FILES.getlist('myfiles')
        #print files
        date_dossier = request.POST.get('date_projet', '')
        cat = request.POST.get('cat', '').lower()
        projet = request.POST.get('dossier', '').lower()
        dossier = cat+"/"+str(date_dossier)+'_'+str(projet).lower()
        efface = request.POST.get('efface', '').lower()
        lien = request.POST.get('lien', '')
        titre_video = request.POST.get('titre_video', '').lower()

        # efface tous les repertoires images du dossier
        try:
            if os.path.exists(racine+dossier+'/thumb'):
                shutil.rmtree(racine+dossier+'/thumb')
            time.sleep(3)
            if os.path.exists(racine+dossier+'/hr'):
                shutil.rmtree(racine+dossier+'/hr')
        except:
            pass

        try:
            # creation des repertoires nécessaires
            if not os.path.exists(racine+dossier+'/hr'):
                os.makedirs(racine+dossier+'/hr')
            if not os.path.exists(racine+dossier+'/thumb'):
                os.makedirs(racine+dossier+'/thumb')
            if not os.path.exists(racine+dossier+'/txt/fr'):
                os.makedirs(racine+dossier+'/txt/fr')
            if not os.path.exists(racine+dossier+'/txt/us'):
                os.makedirs(racine+dossier+'/txt/us')

            if os.path.isfile(racine+dossier+'/txt/us/titre_us.html'):
                pass
            else:
                destination = open(racine+dossier+'/txt/us/titre_us.html', 'w')
                destination.write('')  # ici coller
                destination.close()

            if os.path.isfile(racine+dossier+'/txt/us/fiche_us.html'):
                pass
            else:
                destination = open(racine+dossier+'/txt/us/fiche_us.html', 'w')
                destination.write('')
                destination.close()

            if os.path.isfile(racine+dossier+'/txt/us/desc_us.html'):
                pass
            else:
                destination = open(racine+dossier+'/txt/us/desc_us.html', 'w')
                destination.write('')
                destination.close()
        except:
            return HttpResponse("<br><br><br><br><br><br><br><br><br><br><br>Probleme avec creation du squelette ")
        # time.sleep(5)
        for f in files:
            # ------------------------------- si c'est du html uniquement
            globa = globa+str(f)+" "
            if str(f)[-5:] == '.html':
                try:
                    destination = open(
                        racine+dossier+'/txt/us/%s' % f.name, 'wb+')
                    for chunk in f.chunks():
                        destination.write(chunk)
                    destination.close()
                except:
                    return HttpResponse("<br><br><br><br><br><br><br><br><br><br><br>Probleme avec fichier texte "+globa)

            # ---------------------------------traitement des jpg uniquement
            original = f
            f = str(f).lower().replace(" ", "_")
            if f[-4:] == '.jpg':

                try:
                    image = Image.open(original)
                    w, h = image.size
                    ratio = w/float(h)
                    new_height_thumb = int(720/float(ratio))
                    new_height_full = int(1800/float(ratio))
                    imgthumb = image.resize(
                        (720, new_height_thumb), Image.ANTIALIAS)
                    imgthumb_crop = imgthumb.crop((0, 0, 720, 509))
                    if cat == "videos":
                        imgthumb_crop = imgthumb_crop.crop((0, 60, 720, 450))
                    imgthumb_crop.save(
                        racine+dossier+'/thumb/'+leprojet+"_"+f, 'JPEG', quality=30)
                    imgfull = image.resize(
                        (1800, new_height_full), Image.ANTIALIAS)
                    imgfull.save(racine+dossier+'/hr/'+leprojet +
                                 "_"+f, 'JPEG', quality=30)
                except:
                    return HttpResponse("<br><br><br><br><br><br><br><br><br><br><br>Probleme avec le fichier :" + f + cat)
        # traitement des videos
        if titre_video > '':
            try:
                destination = open(
                    racine+dossier+'/txt/us/titre_us.html', 'wb+')
                destination.write(titre_video)
                destination.close()
            except:
                return HttpResponse("<br><br><br><br><br><br><br><br><br><br><br>Probleme avec titre fichier video ")
        if lien > '':
            try:
                destination = open(racine+dossier+'/txt/us/lien.txt', 'wb+')
                destination.write(lien)
                destination.close()
            except:
                return HttpResponse("<br><br><br><br><br><br><br><br><br><br><br>Probleme avec lien fichier video ")
        return HttpResponseRedirect("/projects/")
        # return HttpResponse("<br><br><br><br><br><br><br><br><br><br><br>Le dossier est bien tranféré")
    sourcetxt = dos
    if os.path.isfile(do+"/source.txt"):
        sourcefic = open(do+"/source.txt", "r")
        sourcetxt = sourcefic.readlines()[0]
        # sourcetxt = sourcetxt.replace("\\","\")

    return render(request, "creation.html", {'cat': cat, 'date_projet': ladate, 'proj': leprojet, 'sourcetxt': sourcetxt, 'images': 'ima'})


def visiteurs_liste(request):
    visiteurs = Visiteur.objects.all().order_by(
        '-test')  # Nous sélectionnons tous nos articles
    cpt = Visiteur.objects.all().count()
    form = VisiteurForm()
    args = {"cpt": cpt}
    args['form'] = form  # important ne pas mettre = DonateurForm()

    # fichier = codecs.open(static+"fichiervisiteur.txt", "r")
    # lignes = fichier.readlines()
    # for ligne in lignes:
    #     if ligne > " ":
    #         ip = ligne.split(',')[1]
    #         email = ligne.split(',')[2]
    #         #page =  ligne.split(',')[3]
    #         date = ligne.split(',')[3]
    #         Visiteur(ip = ip,email = email,page = date).save()

    return render(request, 'visiteurs_liste.html', args)


def merci(request):
    return render(request, 'merci.html')


def upphocv(request):
    # upload photo cv
    if request.method == "POST":
        # recupere les valeurs de la form
        files = request.FILES.getlist('myfiles')
        image = Image.open(files[0])
        size = (1800, 1800)
        image.thumbnail(size)
        os.remove(static + '/cv/hr/cvimg.jpg')
        image.save(static+'cv/hr/cvimg.jpg', 'JPEG')
        return HttpResponseRedirect("/cv")
    return render(request, "upphocv.html", {})


def upphocont(request):
    # upload photo cv
    if request.method == "POST":
        # recupere les valeurs de la form
        files = request.FILES.getlist('myfiles')
        image = Image.open(files[0])
        size = (1800, 1800)
        image.thumbnail(size)
        os.remove(static + '/contact/hr/contimg.jpg')
        image.save(static+'contact/hr/contimg.jpg', 'JPEG')
        return HttpResponseRedirect("/contact")
    return render(request, "upphocont.html", {})


def testdossier(request, dossier):
    return HttpResponse(dossier)


def htmltxt(request, dossier):

    r = requests.get("https://vincent.callebaut.org/static/" +
                     dossier+"txt/us/titre_us.html")
    r.encoding = ('UTF-8')

    texte = r.text
    texte = re.sub('<[^<]+?>', '', texte)
    texte = texte.strip()
    #texte.encoding = ('UTF-8')
    # return HttpResponse(texte)
    return (texte)


def googleUpdate(request):
    deschtm2txt(request)
    titlehtm2txt(request)
    return HttpResponseRedirect("/index")


def deschtm2txt(request):
    cats = ['projects', 'exhibitions', 'publications', 'videos']
    cpt = 0
    for categorie in cats:
        projets = os.listdir(static + categorie + "/")
        for projet in projets:
            cpt = cpt+1
            r = requests.get('https://vincent.callebaut.org/static/' +
                             categorie+'/'+projet+'/txt/us/titre_us.html')
            r.encoding = ('UTF-8')
            test = r.text
            test = test.replace('\n', " ")
            test = re.sub('<[^<]+?>', '', test).strip()
            with io.open(static+categorie+'/'+projet+'/txt/us/descnew.txt', 'w', encoding='UTF-8') as f:
                f.write(test)
                f.close()
        time.sleep(2)
    return HttpResponse(str(cpt)+' '+test)


def titlehtm2txt(request):
    cats = ['projects', 'exhibitions', 'publications', 'videos']
    #cats = ['projects']
    cpt = 0
    for categorie in cats:
        projets = os.listdir(static + categorie + "/")
        for projet in projets:
            cpt = cpt+1
            r = requests.get('https://vincent.callebaut.org/static/' +
                             categorie+'/'+projet+'/txt/us/titre_us.html')
            r.encoding = ('UTF-8')
            texte = r.text
            pos1 = texte.find("</h3>")
            texte = texte[:pos1]
            texte = re.sub('<[^<]+?>', '', texte).strip()
            with io.open(static+categorie+'/'+projet+'/txt/us/titlenew.txt', 'w', encoding='UTF-8') as f:
                f.write(texte)
                f.close()
        time.sleep(2)
    return HttpResponse(str(cpt)+' '+texte)


def _metadesc(request, categorie, projet):
    try:
        lien = static + categorie+'/'+projet+'/txt/us/descnew.txt'
        with io.open(lien, 'r', encoding='utf8') as f:
            myfile = f.readline().strip()
        return myfile
    except:
        return ''


def _metatitle(request, categorie, projet):
    try:
        lien = static + categorie+'/'+projet+'/txt/us/titlenew.txt'
        with io.open(lien, 'r', encoding='utf8') as f:
            myfile = f.readline().strip() + " - Vincent Callebaut Architectures"
        return myfile
    except:
        return ''


def metatest(request):
    #myfile = _metadesc(request,'publications','201130_adn')

    categorie = 'publications'
    projet = '201130_adn'
    lien = static + categorie+'/'+projet+'/txt/us/descnew.txt'
    with io.open(lien, 'rt', encoding='UTF-8') as f:
        myfile = f.readline().strip()
    myfile = re.sub('<[^<]+?>', '', myfile).strip()
    # return myfile
    #returncategorie = 'projects'
    #projet = '130601_swallow'
    #lien = "https://vincent.callebaut.org/static/projects/130601_swallow/txt/us/descnew.txt"
    #lien = static + categorie+'/'+projet+'/txt/us/descnew.txt'
    # with io.open(lien, 'r',encoding='utf8') as f:
    #myfile = f.readline()
    args = {"meta_desc": myfile}
    args['title'] = "L'ADN test"
    return render(request, 'metatest.html', args)
    # return HttpResponse(myfile)


def publicationstest(request, categorie='publications', mode=None):
    litmax = 150
    ip = _ip_visiteur(request)
    cook = _lacook(request)
    form = VisiteurForm()
    envisite = Visiteur(page='pulications', ip=ip, test=dh(request))
    envisite.save()

    modif = request.COOKIES.get('modif')

    racine = static + categorie+"/"
    dossier_projets = static + categorie + "/"
    liste_projets = os.listdir(dossier_projets)
    liste_projets.sort(reverse=True)
    item_list = []
    cpt = 0
    for date_projet in liste_projets:
        cpt = cpt+1
        if cpt >= litmax:
            break
        img_alt = _imgalttxt(request, categorie, date_projet)
        dossier = categorie+"/"+date_projet+"/"
        desc_txt = htmltxt(request, dossier)
        meta_desc = _metadesc(request, categorie, date_projet)
        desc_txt = meta_desc
        desc = ''

        # on recherche les images dns dossier hr
        cpt = cpt+1

        liste_images = os.listdir(dossier_projets+"/"+date_projet+'/hr/')
        liste_images.sort(reverse=False)
        try:
            vignette = liste_images[0]
            title_href = vignette[:-4]
        except:
            vignette = 'pbvig'
            title_href = ""
        projet = date_projet[7:len(date_projet)]  # on enleve la date du debut
        titre = ['pas de titre']
        untitre = ""
        try:
            #tit = os.listdir(racine+date_projet+"/txt/us/")
            # if 'tit' in tit[0]:
            #titrer = codecs.open(racine+date_projet+"/txt/us/"+tit[0], "r")
            titrer = codecs.open(racine+date_projet +
                                 "/txt/us/titre_us.txt", "r")
            untitre = titrer.readline()
            titre = titrer.readlines()
        except:
            titre = ['pas de titre']
            untitre = ""
            pass
        try:
            # titre sous vignette
            titre_lien = categorie+"/"+date_projet+"/txt/us/titre_us.html"
        except:
            titre_lien = "erreur2.html"

        try:
            fic_lien = codecs.open(racine+date_projet+"/txt/us/lien.txt", "r")
            lien = fic_lien.readline()
        except:
            lien = date_projet

        untitreesp = "VCA"
        try:
            untitreesp = untitre.replace(',', ' ')
            untitreesp = untitreesp.replace(' ', '_')
        except:
            pass

        vignette_desc = ""

        proj_titre = [date_projet]
        proj_titre.append(projet)
        proj_titre.append(vignette)
        proj_titre.append(titre_lien)
        proj_titre.append(vignette_desc)
        proj_titre.append(titre)
        proj_titre.append(lien)
        proj_titre.append(title_href)
        proj_titre.append(untitreesp)
        proj_titre.append(cook)
        proj_titre.append(img_alt)
        proj_titre.append(meta_desc)
        item_list.append(proj_titre)
    if categorie == 'projects':
        #meta_desc = "All PUBLICATIONS Vincent Callebaut Architectures Paris"
        menu = 'Projects'
        description = "Vincent Callebaut Architectures, Sustainable Architecture, Biomimicry Design, Paris Smart City 2050, Lilypad, Dragonfly, Tao Zhu Yin Yuan, Agora Garden"
        canonical = canon+'category/projects'
    if categorie == 'videos':
        menu = 'Videos'
        title = "All Vidéos"
        #meta_desc = "All Videos Vincent Callebaut Architectures Paris"
        description = "Vincent Callebaut Architectures, Talks, TEDx, TV Interviews, TF1, France 2, Arte, M6, LCP, City of Future, Sustainability, Energy Plus, Circular Economy"
        canonical = canon+"category/videos"
    if categorie == 'exhibitions':
        #meta_desc = "All exhibitions Vincent Callebaut Architectures Paris"
        menu = 'Exhibitions'
        description = "Vincent Callebaut Architectures, Exhibitions, Conferences, Lectures, International Architecture, Innovation Awards, Architecture Biennial, World Exhibition"
        canonical = canon+"category/exhibitions"
    if categorie == 'publications':
        #meta_desc = "All publications Vincent Callebaut Architectures Paris,-"
        menu = 'Publications'
        description = "Vincent Callebaut Architectures, Press Releases, Monographies, Books, Paris 2050, Fertile Cities, Archibiotic, Interviews, CNN, BBC, Time, Green Building"
        canonical = canon+"category/publications"

    title = categorie.capitalize()   # aussi utilisé our video
    if cpt < 5:
        vigdef = 'min'
    else:
        vigdef = 'full'
    args = {"untitreesp": 'test'}
    args['description'] = description
    args['item_list'] = item_list
    args['categorie'] = categorie
    args['mode'] = mode
    args['form'] = form
    args['title'] = title
    args['menu'] = menu
    args['meta_titre'] = "PUBLICATIONS"
    args['meta_desc'] = meta_desc
    #args['canonical']= canonical
    args['vignette'] = "vignette"
    args['titre_lien'] = titre_lien
    tup = listlast(request)
    args['tup'] = tup
    args['cook'] = cook
    args['vigdef'] = vigdef
    return render(request, 'publications.html', args)
