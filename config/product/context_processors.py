from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart = None

    return {
        "cart": cart
    }
