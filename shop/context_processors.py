from .models import Cart


def cart_items_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {'cart_items': cart.cartitem_set.all()}
        except Cart.DoesNotExist:
            return {'cart_items': []}
    return {'cart_items': []}
