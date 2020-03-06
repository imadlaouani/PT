
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage
from PT.forms import *
from PT.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.contrib.auth.forms import UserCreationForm


def inscription_vendeur(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST,request.FILES)
        if form.is_valid():
            form.save() #Sauvegarde/Creation d'un utilisateur de base
            username = form.cleaned_data.get('username')
            mail = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
             #Authentification de l'utilisateur
            user = authenticate(username=username, password=raw_password)
            Utilisateur = User.objects.get(username=username)
            #On crée un vendeur 
            vendeur = Vendeur(numVendeur=Utilisateur,nomVendeur=form.cleaned_data.get('last_name'),prenomVendeur=form.cleaned_data.get('first_name'), mailVendeur=form.cleaned_data.get('email'),photoVendeur=form.cleaned_data.get('photo'))
            vendeur.save()
            #On crée un acheteur 
            acheteur = Acheteur(numAcheteur=Utilisateur,nomAcheteur=form.cleaned_data.get('last_name'),prenomAcheteur=form.cleaned_data.get('first_name'), mailAcheteur=form.cleaned_data.get('email'),adresseAcheteur=form.cleaned_data.get('adresse'))
            acheteur.save()
            login(request, user) #Connexion au site
            messages.success(request, f'Vous êtes inscrits {username}!')
            return redirect('home')
    else:
        form = InscriptionForm()
        #u_form = UserCreationForm()
    return render(request,'comptes/inscription_vendeur.html',{'form':form})

def inscription_acheteur(request):
    if request.method == 'POST':
        form = AcheteurForm(request.POST)
        if form.is_valid():
            form.save() #Sauvegarde/Creation d'un utilisateur de base
            username = form.cleaned_data.get('username')
            mail = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
             #Authentification de l'utilisateur
            user = authenticate(username=username, password=raw_password)
            Utilisateur = User.objects.get(username=username)
            acheteur = Acheteur(numAcheteur=Utilisateur,nomAcheteur=form.cleaned_data.get('last_name'),prenomAcheteur=form.cleaned_data.get('first_name'), mailAcheteur=form.cleaned_data.get('email'),adresseAcheteur=form.cleaned_data.get('adresseAcheteur'))
             # On ajoute l'utilisateur au groupe 
            acheteur.save()
            login(request, user) #Connexion au site
            return redirect('home')
    else:
        form = AcheteurForm()
    return render(request,'comptes/inscription_acheteur.html',{'form':form})

def inscription(request):

    return render(request,'comptes/inscription.html')

def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
		# On récupère et connecte l'utilisateur
            user = form.get_user()
            login(request,user)
            return redirect('home')

    else:
        form = AuthenticationForm()
        return render(request,'comptes/connexion.html',{'form':form})

def logout_user(request):
    logout(request)
    return render(request, 'comptes/deconnexion.html')


@login_required
def profil(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        form = VendeurForm(request.POST,request.FILES, instance=request.user.vendeur)
        if form.is_valid() and u_form.is_valid():
            form.save()
            u_form.save()
            messages.success(request, f'Votre compte a bien été modifié !')
            return redirect('comptes:profil')

    else:
        form = VendeurForm()
        u_form = UserUpdateForm()

    return render(request, 'comptes/profil.html', {"form":form,"u_form":u_form})

class VendeurDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vendeur
    template_name = 'comptes/vendeur_supprimer.html'
    success_url = '/'