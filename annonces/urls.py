from django.urls import path,include
from django.conf import settings
from annonces import views
from django.conf.urls import url,include
from annonces.views import ProduitCreateView,ProduitUpdateView,ProduitDeleteView

urlpatterns = [
    url(r'^mes_annonces/$', views.mes_annonces,name="mes_annonces"),
    path('encherir/<int:idProduit>/', views.encherir),
    path('ajouter/', ProduitCreateView.as_view(),name="produit_ajouter"),
    path('<int:pk>/modifier/', ProduitUpdateView.as_view(),name="produit_modifier"),
    path('<int:pk>/supprimer/', ProduitDeleteView.as_view(),name="produit_supprimer"),
    path('<int:pk>/encherir/', views.encherir,name="produit_encherir"),
    url(r'^$', views.liste_produits,name="liste_produits"),
    path('<int:pk>/', views.produit_detail,name="produit_detail"),
    path('categorie/<str:categorie>/', views.filtre_categorie,name="produits_categorie"),

    
    
   ]
