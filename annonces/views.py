from django.shortcuts import render
from PT.forms import ProduitForm,EnchereForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from PT.models import *
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.storage import FileSystemStorage
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)





class ProduitCreateView(LoginRequiredMixin, CreateView):
    model = Produit
    template_name = 'annonces/produit_ajouter.html'
    fields = ['titre', 'description','images','prixBase','dateDebut','dateFin','categorie']

    def form_valid(self, form):
        form.instance.vendeurFK= self.request.user.vendeur
        return super().form_valid(form)


class ProduitUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Produit
    template_name = 'annonces/produit_ajouter.html'
    fields = ['titre', 'description','images','prixBase','categorie']

    def form_valid(self, form):
        form.instance.vendeurFK = self.request.user.vendeur
        return super().form_valid(form)

    def test_func(self):
        produit = self.get_object()
        if self.request.user.vendeur == produit.vendeurFK:
            return True
        return False


class ProduitDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Produit
    template_name = 'annonces/produit_supprimer.html'
    success_url = '/'

    def test_func(self):
        produit = self.get_object()
        if self.request.user.vendeur == produit.vendeurFK:
            return True
        return False



@login_required
def mes_annonces(request):
    # On récupère tous les produits d'un vendeur
    vendeur = Vendeur.objects.get(numVendeur=request.user)
    listeProduits = Produit.objects.filter(vendeurFK=vendeur)
    return render(request, 'annonces/mes_annonces.html', locals())

def liste_produits(request):
    produits = []
    for i in Produit.objects.filter(dateFin__gte = timezone.now()):
        produits.append(i)

    return render(request, 'annonces/liste_produits.html',{'produits':produits})

def produit_detail(request,pk):
    produit = Produit.objects.get(numProduit=pk)
    encheres =[]
    for i in Enchere.objects.filter(produitFK=pk):
        encheres.append(i)

    return render(request, 'annonces/produit_detail.html',{'produit':produit,'encheres':encheres})

@login_required
def encherir(request,pk):
    produit = Produit.objects.get(numProduit=pk)
    if produit.dateFin>= timezone.now():
        if request.method == 'POST':
            form = EnchereForm(request.POST)
            if form.is_valid():
                enchere = Enchere(acheteurFK = request.user.acheteur,produitFK = produit,montant = form.cleaned_data["montant"],commentaire = form.cleaned_data["commentaire"],moment=timezone.now())
                enchere.save()
                produit.totalEnchere +=form.cleaned_data["montant"]
                produit.acheteurFK=request.user.acheteur
                produit.save()
                return redirect('liste_produits')

        else:
            form = EnchereForm(request.POST)
            return render(request, 'annonces/produit_encherir.html', locals())


def filtre_categorie(request, categorie):
   
    produits = []
    if categorie == "Véhicules":
        for i in Produit.objects.filter(dateFin__gte=timezone.now(), categorie="Véhicules"):
            produits.append(i)

    elif categorie == "Vacances":
        for i in Produit.objects.filter(dateFin__gte=timezone.now(), categorie="Vacances").order_by('dateFin'):
            produits.append(i)

    elif categorie == "Loisirs":
        for i in Produit.objects.filter(dateFin__gte=timezone.now(), categorie="Loisirs").order_by('dateFin'):
            produits.append(i)

    elif categorie == "Mode":
        for i in Produit.objects.filter(dateFin__gte=timezone.now(), categorie="Mode").order_by('dateFin'):
            produits.append(i)

    elif categorie == "Multimédia":
        for i in Produit.objects.filter(dateFin__gte=timezone.now(), categorie="Multimédia").order_by('dateFin'):
            produits.append(i)

    elif categorie == "Maison":
        for i in Produit.objects.filter(dateFin__gte=timezone.now(), categorie="Maison").order_by('dateFin'):
            produits.append(i)

    elif categorie == "Autre":
        for i in Produit.objects.filter(dateFin__gte=timezone.now(), categorie="Autre").order_by('dateFin'):
            produits.append(i)

    
    return render(request, 'annonces/produits_categorie.html', {'produits': produits})