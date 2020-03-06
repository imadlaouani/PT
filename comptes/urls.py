from django.conf.urls import url
from django.urls import path
from comptes import views 
app_name = 'comptes'

urlpatterns = [
	url(r'^inscription/$',views.inscription, name ='inscription'),
	url(r'^acheteur/inscription/$',views.inscription_acheteur, name ='inscription_acheteur'),
	url(r'^vendeur/inscription/$',views.inscription_vendeur, name ='inscription_vendeur'),
	url(r'^connexion/$',views.connexion, name ='connexion'),
	url(r'^deconnexion/$',views.logout_user, name ='deconnexion'),
	url(r'^profil/$',views.profil, name ='profil'),
	#url(r'^supprimer/$',views.VendeurDeleteView, name ='vendeur_supprimer'),
	path('<int:pk>/supprimer/', views.VendeurDeleteView, name ='vendeur_supprimer'),


	
]