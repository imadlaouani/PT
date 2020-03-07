from django.conf.urls import url
from django.urls import path
from comptes import views 
app_name = 'comptes'

urlpatterns = [
	url(r'^inscription/$',views.inscription, name ='inscription'),
	url(r'^connexion/$',views.connexion, name ='connexion'),
	url(r'^deconnexion/$',views.logout_user, name ='deconnexion'),
	url(r'^profil/$',views.profil, name ='profil'),
	#url(r'^supprimer/$',views.VendeurDeleteView, name ='vendeur_supprimer'),
	path('supprimer/<int:pk>/', views.compte_supprimer, name ='compte_supprimer'),


	
]