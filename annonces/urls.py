from django.urls import path,include
from django.conf import settings
from annonces import views
from django.conf.urls import url,include
from annonces.views import ProduitCreateView,ProduitUpdateView,ProduitDeleteView

urlpatterns = [
    #url(r'^ajouter/$', views.ajouter_annonce,name="ajouter_annonce"),
    url(r'^upload/$', views.upload,name="upload"),
    url(r'^mes_annonces/$', views.mes_annonces,name="mes_annonces"),
    #url(r'^$', views.liste_annonces,name="liste_annonces"),
    path('encherir/<int:idProduit>/', views.encherir),
    #url(r'^$', ProduitListView.as_view(),name="liste_produits"),
    #path('<int:pk>/', ProduitDetailView.as_view(),name="produit_detail"),
    path('ajouter/', ProduitCreateView.as_view(),name="produit_ajouter"),
    path('<int:pk>/modifier/', ProduitUpdateView.as_view(),name="produit_modifier"),
    path('<int:pk>/supprimer/', ProduitDeleteView.as_view(),name="produit_supprimer"),
    path('<int:pk>/encherir/', views.encherir,name="produit_encherir"),
    url(r'^$', views.liste_produits,name="liste_produits"),
    path('<int:pk>/', views.produit_detail,name="produit_detail"),

    
    
   ]