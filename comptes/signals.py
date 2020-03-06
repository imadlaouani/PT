from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Acheteur


@receiver(post_save, sender=Vendeur)
def creer_acheteur(sender, instance, created, **kwargs):
    if created:
        Acheteur.objects.create(numAcheteur=instance,nomAcheteur=instance.nomVendeur,prenomVendeur=instance.prenomVendeur,mailAcheteur=instance.mailVendeur,photoAcheteur=photoVendeur)


@receiver(post_save, sender=Vendeur)
def save_acheteur(sender, instance, **kwargs):
    instance.acheteur.save()