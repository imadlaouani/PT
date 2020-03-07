from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image
from django.urls import reverse



class Vendeur(models.Model):
    numVendeur = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    nomVendeur = models.CharField(max_length=30)
    prenomVendeur = models.CharField(max_length=30)
    mailVendeur = models.EmailField()
    photoVendeur = models.ImageField(default= 'default.jpg',upload_to= "photosdeprofil")

    def __str__(self):
        return f'{self.numVendeur.username} Vendeur' 

    def save(self):
        super().save()

        img = Image.open(self.photoVendeur.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photoVendeur.path)

    class Meta:
        db_table ='vendeur'


class Acheteur(models.Model):
    numAcheteur = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    nomAcheteur = models.CharField(max_length=30)
    prenomAcheteur = models.CharField(max_length=30)
    mailAcheteur = models.EmailField()
    adresseAcheteur = models.TextField(null=True)
    photoAcheteur = models.ImageField(default= 'default.jpg',upload_to= "photosdeprofil",blank = True)

    def __str__(self):
        return f'{self.numAcheteur.username} Acheteur' 


class Produit(models.Model):
    Categorie_choices = [
    ('Véhicules', 'Véhicules'),
    ('Vacances', 'Vacances'),
    ('Loisirs', 'Loisirs'),
    ('Mode', 'Mode'),
    ('Multimédia', 'Multimédia'),
    ('Maison', 'Maison'),
    ('Autre', 'Autre'),
]
    numProduit = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=30)
    description = models.TextField(verbose_name="Description du produit")
    images = models.ImageField(upload_to= "images", height_field=None)
    prixBase =  models.FloatField(validators=[MinValueValidator(0)],verbose_name="Mise à prix")
    totalEnchere =  models.FloatField(null=True,default=0,validators=[MinValueValidator(0)])
    dateDebut = models.DateTimeField(default=timezone.now, verbose_name="Date de début de l'enchère")
    dateFin = models.DateTimeField(verbose_name="Date de fin de l'enchère")
    vendeurFK = models.ForeignKey(Vendeur, on_delete=models.CASCADE, db_column='numVendeur')
    acheteurFK = models.ForeignKey(Acheteur,null=True,blank=True, on_delete=models.CASCADE, db_column='acheteurFK')
    categorie = models.CharField(max_length=30, choices=Categorie_choices)

    def __str__(self):
        return f'{self.titre}' 

    def save(self):
        if self.images:
            super().save()

            img = Image.open(self.images.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.images.path)

    def get_absolute_url(self):
        return reverse('produit_detail', kwargs={'pk': self.pk})


class Enchere(models.Model):
    acheteurFK = models.ForeignKey(Acheteur, on_delete=models.CASCADE, db_column='numAcheteur')
    produitFK = models.ForeignKey(Produit, on_delete=models.CASCADE, db_column='numProduit')
    numEnchere = models.AutoField(primary_key=True)
    moment = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=6, decimal_places=1,validators=[MinValueValidator(0.5)],verbose_name="Montant de l'enchère")
    commentaire = models.CharField(max_length=50,null=True)
    

    class Meta:
        db_table = 'Enchere'
    
