from django.shortcuts import render
from django.http import HttpResponse, Http404 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage
from PT.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

def home(request):

    # Pour un vendeur on lui affiche ses ventes et/ou ses invendus et/ou ses annonces sur la page d'accueil
    mes_annonces = []
    ventes = []
    invendus = []
    produits_encheris=[]
    enchere_gagnees =[]
    encheres = []
    if request.user.is_authenticated:
        # Pour un vendeur ses ventes
        for i in Produit.objects.filter(vendeurFK=request.user.vendeur,dateFin__lte = timezone.now(),totalEnchere__gt=0):
            ventes.append(i)
        # ses invendus
        for j in Produit.objects.filter(vendeurFK=request.user.vendeur,dateFin__lte = timezone.now(),totalEnchere=0):
            invendus.append(j)
        # ses annonces en cours
        for k in Produit.objects.filter(vendeurFK=request.user.vendeur,dateFin__gt = timezone.now()):
            mes_annonces.append(k)
        # Pour un acheteur ses encheres remportées       
        for a in Produit.objects.filter(acheteurFK=request.user.acheteur,dateFin__lte=timezone.now()):
            enchere_gagnees.append(a)
        # ses encheres
        for c in Enchere.objects.filter(acheteurFK=request.user.acheteur):
            encheres.append(c.produitFK)

        # ensemble des produits auxquels l'acheteur a enchéris et dont l'enchère est terminée 
        """for k in range(0,len(encheres)):
            for b in Produit.objects.filter(numProduit=encheres[k],dateFin__lte=timezone.now()):
                produits_encheris.append(b)"""

    return render(request, 'home.html',locals())





def inscription(request):
    error = False

    if request.method == "POST":
        form = AcheteurForm(request.POST)
        form.save()
        if form.is_valid():
            #On inscrit l'acheteur
            acheteur = Acheteur(nomAcheteur=form.cleaned_data['last_name'], prenomAcheteur=form.cleaned_data['first_name'],mailAcheteur = form.cleaned_data['email'],adresseAcheteur = form.cleaned_data['adresseAcheteur'])
            acheteur.save()
            # On le connecte
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            login(request, authenticate(username=username, password=password))  # nous connectons l'utilisateur
            
    else:
        form = AcheteurForm()

    return render(request, 'inscription.html', locals())


