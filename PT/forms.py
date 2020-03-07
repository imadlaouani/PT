from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PT.models import *
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator




class ConnexionForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

# Formulaire d'inscription ou de modification d'un acheteur
class AcheteurForm(UserCreationForm):
    adresseAcheteur = forms.CharField(max_length=254)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1', 'password2' )

# Formulaire d'inscription ou de modification d'un vendeur
class VendeurForm(forms.ModelForm):
    class Meta:
        model = Vendeur
        fields = ['photoVendeur']

# Formulaire de création ou de modification d'un produit
class ProduitForm(forms.Form):
    Categorie_choices = (
        ('Emploi', 'Véhicules'),
        ('Vacances', 'Loisirs'),
        ('Mode', 'Multimédia'),
        ('Maison', 'Autre')
    )
    titre = forms.CharField(max_length=30)
    description = forms.CharField(max_length=254)
    images = forms.ImageField(max_length=400,required = False)
    prixBase =  forms.FloatField(validators=[MinValueValidator(0)])
    dateDebut = forms.DateTimeField(label="Date de début de l'enchère")
    dateFin = forms.DateTimeField()
    categorie = forms.ChoiceField(label="Catégorie",choices=Categorie_choices)

# Formulaire de création d'une enchère
class EnchereForm(forms.Form):
    montant = forms.FloatField(validators=[MinValueValidator(0.5)])
    commentaire = forms.CharField(max_length=50)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Adresse électronique")
    class Meta:
        model = User
        fields = ['username','email' ]


# Formulaire d'inscription
class InscriptionForm(UserCreationForm):
    photo = forms.ImageField(required=False)
    adresse = forms.CharField(widget=forms.Textarea,required=False)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1', 'password2' )