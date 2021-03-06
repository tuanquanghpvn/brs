from django.conf import settings

from apps.books.models import Book


def get_cart(request):
    """
    Get cart session or create an empty cart if not exist.
    """
    cart = request.session.get(settings.CART)
    if cart is None:
        request.session[settings.CART] = {}
        cart = request.session[settings.CART]
    return cart

def get_books(request):
    cart = get_cart(request)
    books = Book.objects.filter(id__in=cart.keys())
    return books
