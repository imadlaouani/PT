
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


def inscription(request):
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
            if(form.cleaned_data.get('photo') == None) :
                photo='default.jpg'
            else :
                photo=form.cleaned_data.get('photo')
            vendeur = Vendeur(numVendeur=Utilisateur,nomVendeur=form.cleaned_data.get('last_name'),prenomVendeur=form.cleaned_data.get('first_name'), mailVendeur=form.cleaned_data.get('email'),photoVendeur=photo)
            vendeur.save()
            #On crée un acheteur 
            acheteur = Acheteur(numAcheteur=Utilisateur,nomAcheteur=form.cleaned_data.get('last_name'),prenomAcheteur=form.cleaned_data.get('first_name'), mailAcheteur=form.cleaned_data.get('email'),photoAcheteur=photo,adresseAcheteur=form.cleaned_data.get('adresse'))
            acheteur.save()
            login(request, user) #Connexion au site
            messages.success(request, f'Vous êtes inscrits {username}!')
            return redirect('home')
    else:
        form = InscriptionForm()
    return render(request,'comptes/inscription.html',{'form':form})


def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(data=request.POST)
        if form.is_valid():
		# On récupère et connecte l'utilisateur
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request,user)
                return redirect('home')
            else :
                messages.warning(request, f'Utilisateur inconnu ou mauvais de mot de passe.')


    else:
        form = ConnexionForm()
    return render(request,'comptes/connexion.html',{'form':form})

@login_required
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
    template_name = 'comptes/compte_supprimer.html'
    success_url = '/'


def compte_supprimer(request,pk):
    if request.method =="POST":
        request.user.delete()
        logout(request)
        return redirect('home')

    return render(request, 'comptes/compte_supprimer.html')