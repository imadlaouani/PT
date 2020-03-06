from django.shortcuts import render

# Create your views here.

from PT.forms import ProduitForm,EnchereForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from PT.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.storage import FileSystemStorage
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)




"""
class ProduitDetailView(DetailView):
    model = Produit
    template_name = 'annonces/produit_detail.html'
    context_object_name = 'produit'

   """ 


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






def ajouter_annonce(request):
    """if !(request.session['estEtu']):
        return render(request, 'error404.html')
    else:"""
    if request.method == 'POST':
        utilisateur = User.objects.get(id=request.user.id)
        form = ProduitForm(request.POST,request.FILES)
        if form.is_valid():
            vendeur = Vendeur.objects.get(numVendeur=request.user)
            produit = Produit(titre=form.cleaned_data["titre"],description = form.cleaned_data["description"],images = request.FILES['images'],prixBase = form.cleaned_data["prixBase"],dateDebut = form.cleaned_data["dateDebut"],dateFin=form.cleaned_data["dateFin"],vendeurFK=vendeur,categorie = form.cleaned_data["categorie"])
            produit.save()
            return redirect('home')
    else:
        form = ProduitForm()
    return render(request, 'annonces/ajouter.html', locals())

def upload(request):
    if request.method == 'POST':
        image = request.FILES['images']
        photo = FileSystemStorage()
        photo.save(image.name,image)

    return render(request,'annonces/upload.html')

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

