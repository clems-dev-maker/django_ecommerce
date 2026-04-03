from .models import Cart

# def cart_item_count(request):
#     if request.user.is_authenticated:
#         try:
#             cart = Cart.objects.get(user=request.user)
#             count = sum(item.quantity for item in cart.cartitem_set.all())
#         except Cart.DoesNotExist:
#             count = 0
#     else:
#         count = 0
#
#     return {
#         'cart_count': count
#     }


def cart_data(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            items = cart.cartitem_set.all()
            total = sum(item.product.price * item.quantity for item in items)
            count = sum(item.quantity for item in items)
        except Cart.DoesNotExist:
            items = []
            total = 0
            count = 0
    else:
        items = []
        total = 0
        count = 0

    return {
        'cart_items_nav': items,
        'cart_total': total,
        'cart_count': count,
    }
