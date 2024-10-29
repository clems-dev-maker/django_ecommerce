from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Route pour la liste des produits
    path('', views.product_list, name='product_list'),

    # Route pour les détails d'un produit (avec un paramètre 'slug')
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Routes pour ajouter ou supprimer un produit au panier (avec un paramètre 'product_id')
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),


    # Route pour afficher le panier
    path('cart/', views.cart_detail, name='cart_detail'),

    # Route pour le processus de commande (checkout)
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),  # Ajoute cette ligne pour la vue paiement
    path('order/success/', views.order_success, name='order_success'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
