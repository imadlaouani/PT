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



