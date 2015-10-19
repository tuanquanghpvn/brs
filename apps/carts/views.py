from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from apps.core.views import BaseView
from apps.carts import utils
from apps.carts.forms import BookItem


class ViewCart(BaseView, TemplateView):
    template_name = 'carts/index.html'


class AddBookToCart(FormView):
    form_class = BookItem

    def get(self, request, *args, **kwargs):
        return HttpResponse()
    
    def form_valid(self, form):
        cart = utils.get_cart(self.request)
        book_id = form.cleaned_data['book']
        quantity = form.cleaned_data['quantity']
        exist = cart.get(book_id, False)
        if exist:
            cart[book_id] += quantity
        else:
            cart[book_id] = quantity
        
        book = get_object_or_404(Book, id=book_id)
        return HttpResponseRedirect(reverse('books:detail',
                            kwargs={'pk': book_id, 'slug': book.slug}))
