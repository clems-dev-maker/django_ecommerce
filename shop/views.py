from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
import stripe
from django.conf import settings
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.contrib.auth import login
from django.contrib.auth import logout

from .models import Product, Cart, CartItem, Order, Wishlist, Review


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)

    user_wishlist = []
    if request.user.is_authenticated:
        user_wishlist = Wishlist.objects.filter(user=request.user).values_list('product', flat=True)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'user_wishlist': user_wishlist
    })


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Calcul du nouveau compteur
    cart_count = sum(item.quantity for item in cart.cartitem_set.all())

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart_count
        })

    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    item = CartItem.objects.filter(
        id=item_id,
        cart__user=request.user
    ).first()

    if item:
        item.delete()

    cart = Cart.objects.get(user=request.user)
    items = cart.cartitem_set.all()

    cart_data = [
        {
            "id": i.id,
            "name": i.product.name,
            "price": float(i.product.price),
            "quantity": i.quantity,
            "image": i.product.image.url
        }
        for i in items
    ]

    cart_count = sum(i.quantity for i in items)
    cart_total = sum(i.quantity * i.product.price for i in items)

    return JsonResponse({
        "success": True,
        "cart_items": cart_data,
        "cart_count": cart_count,
        "cart_total": float(cart_total)
    })


@login_required
def update_cart_item(request, item_id, action):
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)

        if action == "increase":
            item.quantity += 1
            item.save()

        elif action == "decrease":
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()

        # Recalcul panier
        cart = item.cart
        cart_items = cart.cartitem_set.all()
        cart_count = sum(i.quantity for i in cart_items)
        cart_total = sum(i.quantity * i.product.price for i in cart_items)

        return JsonResponse({
            "success": True,
            "cart_count": cart_count,
            "cart_total": float(cart_total)
        })

    except CartItem.DoesNotExist:
        return JsonResponse({"success": False})


@login_required
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
    cart = Cart.objects.get(user=request.user)

    cart_items = cart.cartitem_set.all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'shop/payment.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })


@login_required
def toggle_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        wishlist_item.delete()
        status = 'removed'
    else:
        status = 'added'

    return JsonResponse({
        'status': status
    })


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'shop/wishlist.html', {'items': items})


def order_success(request):
    # Si tu passes des informations spécifiques, comme un récapitulatif de la commande
    order = request.session.get('order')  # Exemple de récupération d'infos de la session
    context = {
        'order': order,
    }
    return render(request, 'shop/order_success.html', context)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Connexion automatique
            login(request, user)

            # Email de confirmation
            send_mail(
                subject="Bienvenue sur notre site !",
                message=f"Bonjour {user.username}, votre compte a bien été créé.",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )

            messages.success(request, "Compte créé avec succès !")
            return redirect('product_list')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def custom_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Vous avez été déconnecté avec succès.")
        return redirect('product_list')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/profile.html', {'orders': orders})


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_checkout_session(request):
    cart = Cart.objects.get(user=request.user)

    line_items = []

    for item in cart.cartitem_set.all():
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/order/success/',
        cancel_url='http://127.0.0.1:8000/cart/',
    )

    return JsonResponse({'id': session.id})


@login_required
def add_review(request, product_id):
    if request.method == "POST":
        Review.objects.create(
            product_id=product_id,
            user=request.user,
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment')
        )

    return redirect('product_detail', slug=request.POST.get('slug'))
