from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Cart, CartItem, Order


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')


def remove_from_cart(request, item_id):
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()  # Supprimer l'élément du panier
        messages.success(request, "Le produit a été retiré du panier.")
    except CartItem.DoesNotExist:
        messages.error(request, "L'élément n'existe pas dans votre panier.")

    return redirect('cart_detail')  # Redirige vers la page du panier


def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
    except Cart.DoesNotExist:
        cart_items = None

    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items})


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)

        for item in cart.cartitem_set.all():
            product = item.product

            # Vérifier que le stock est suffisant
            if product.stock < item.quantity:
                messages.error(request, f"Le produit {product.name} n'est pas en stock suffisant.")
                return redirect('cart_detail')

            # Déduire la quantité commandée du stock
            product.stock -= item.quantity
            product.save()

            # Créer une commande et notifier si le stock est bas
            Order.objects.create(
                user=request.user,
                product=product,
                quantity=item.quantity,
                total_price=product.price * item.quantity
            )

            # Vérifier le stock après chaque déduction
            product.check_stock()

        # Vérifier si le panier contient des articles
        if cart.cartitem_set.count() == 0:
            messages.error(request, "Votre panier est vide.")
            return redirect('cart_detail')  # Rediriger vers la page du panier si le panier est vide

        # Redirection vers la page de paiement
        return redirect('payment')  # Remplace 'payment' par le nom de l'URL de ta page de paiement

    except Cart.DoesNotExist:
        messages.error(request, "Votre panier est vide.")
        return redirect('cart_detail')


@login_required
def payment(request):
    try:
        cart = Cart.objects.get(user=request.user)

        if request.method == 'POST':
            # Logique de traitement du paiement ici (via une API comme Stripe, PayPal, etc.)
            # Si le paiement est validé, on crée les commandes

            for item in cart.cartitem_set.all():
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.product.price * item.quantity
                )

            cart.delete()  # Vider le panier après le paiement

            messages.success(request, "Paiement réussi. Merci pour votre commande !")
            return redirect('order_success')  # Rediriger vers la page de succès de la commande

        return render(request, 'shop/payment.html', {'cart': cart})

    except Cart.DoesNotExist:
        messages.error(request, "Votre panier est vide.")
        return redirect('cart_detail')


def order_success(request):
    # Si tu passes des informations spécifiques, comme un récapitulatif de la commande
    order = request.session.get('order')  # Exemple de récupération d'infos de la session
    context = {
        'order': order,
    }
    return render(request, 'shop/order_success.html', context)
