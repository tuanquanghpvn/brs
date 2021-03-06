from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.admin.forms import AdminAuthenticationForm
from django.views.generic import (
        FormView, View, CreateView, DetailView,
        UpdateView, DeleteView, TemplateView, ListView,
)
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

from . import forms
from apps.categories.models import Category
from apps.books.models import Book
from apps.requestbooks.models import RequestedBook
from apps.users.models import UserProfile
from apps.carts.models import Cart, Item

class AdminRequiredMixin(object):
    """docstring for AdminRequiredMixin"""
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)        


class LoginView(FormView):
    form_class = AdminAuthenticationForm
    template_name = 'admin/login.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_active and user.is_staff:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('admin:dashboard')

    def form_valid(self, form):
        admin = form.get_user()
        login(self.request, admin)
        return super().form_valid(form)


class DashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'admin/dashboard_index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        info = {
            'title': 'Dashboard - Book Review System',
            'sidebar': ['dashboard']
        }
        context['info'] = info
        return context

# Categories Management

class CategoryView(AdminRequiredMixin, ListView):
    """docstring for CategoryView"""
    context_object_name = 'list_category'
    template_name = 'admin/category_index.html'    

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        info = {
            'title': 'Category - Book Review System',
            'sidebar': ['category']
        }
        context['info'] = info
        return context

class CategoryCreateView(AdminRequiredMixin, CreateView):
    """docstring for CategoryCreateView"""
    form_class = forms.CategoryForm    
    template_name = 'admin/category_create.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        info = {
            'title': 'Create Category - Book Review System',
            'sidebar': ['category']
        }
        context['info'] = info
        return context

    def get_success_url(self):
        return reverse('admin:list_category')

class CategoryUpdateView(AdminRequiredMixin, UpdateView):
    """docstring for CategoryUpdateView"""
    model = Category
    form_class = forms.CategoryForm    
    template_name = 'admin/category_update.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        info = {
            'title': 'Update Category - Book Review System',
            'sidebar': ['category']
        }
        context['info'] = info
        return context

    def get_success_url(self):
        return reverse('admin:list_category')

class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    """docstring for CategoryDeleteView"""
    model = Category

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:list_category')

# Books Management

class BookView(AdminRequiredMixin, ListView):
    """docstring for BookView"""
    context_object_name = 'list_book'
    template_name = 'admin/book_index.html'    

    def get_queryset(self):
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BookView, self).get_context_data(**kwargs)
        info = {
            'title': 'Book - Book Review System',
            'sidebar': ['book']
        }
        context['info'] = info
        return context

class BookCreateView(AdminRequiredMixin, CreateView):
    """docstring for BookCreateView"""
    form_class = forms.BookForm    
    template_name = 'admin/book_create.html'

    def get_context_data(self, **kwargs):
        context = super(BookCreateView, self).get_context_data(**kwargs)
        info = {
            'title': 'Create Book - Book Review System',
            'sidebar': ['book']
        }
        context['info'] = info
        context['list_category'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse('admin:list_book')

class BookUpdateView(AdminRequiredMixin, UpdateView):
    """docstring for BookUpdateView"""
    model = Book
    form_class = forms.BookForm    
    template_name = 'admin/book_update.html'

    def get_context_data(self, **kwargs):
        context = super(BookUpdateView, self).get_context_data(**kwargs)
        info = {
            'title': 'Update Book - Book Review System',
            'sidebar': ['book']
        }
        context['info'] = info
        context['list_category'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse('admin:list_book')

class BookDeleteView(AdminRequiredMixin, DeleteView):
    """docstring for BookDeleteView"""
    model = Book

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:list_book')

# Requested Books Management

class RequestedBookView(AdminRequiredMixin, ListView):
    """docstring for RequestedBookView"""
    context_object_name = 'list_requested_book'
    template_name = 'admin/requested_book_index.html'

    def get_queryset(self):
        return RequestedBook.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RequestedBookView, self).get_context_data(**kwargs)
        info = {
            'title': 'Requested - Book Review System',
            'sidebar': ['requested_book']
        }
        context['info'] = info
        return context

class RequestedBookDeleteView(AdminRequiredMixin, DeleteView):
    """docstring for RequestedBookDeleteView"""
    model = RequestedBook

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:list_requested_book')

class RequestedBookUpdateView(AdminRequiredMixin, UpdateView):
    """docstring for RequestedBookDetailView"""
    model = RequestedBook
    template_name = 'admin/requested_book_update.html'
    fields = ['title', 'description', 'status', 'categories']    

    def get_context_data(self, **kwargs):
        context = super(RequestedBookUpdateView, self).get_context_data(**kwargs)
        info = {
            'info': {
                'title': 'Update Requested Book',
                'sidebar': ['requested_book']
            },
            'list_category': Category.objects.all(), 
            'list_status': RequestedBook.STATUS_CHOICES,
        }
        context.update(info)
        return context

    def get_success_url(self):
        return reverse_lazy('admin:list_requested_book')

# Users Management

class UserProfileView(AdminRequiredMixin, ListView):
    """docstring for UserProfileView"""
    context_object_name = 'list_user'
    template_name = 'admin/user_profile_index.html'

    def get_queryset(self):
        return UserProfile.objects.all()

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        info = {
            'title': 'User - Book Review System',
            'sidebar': ['user']
        }
        context['info'] = info
        return context

class UserProfileDeleteView(AdminRequiredMixin, DeleteView):
    """docstring for UserProfileDeleteView"""
    model = UserProfile

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:list_user')

class UserProfileDetailView(AdminRequiredMixin, DetailView):
    """docstring for UserProfileDetailView"""
    def __init__(self, arg):
        super(UserProfileDetailView, self).__init__()
        self.arg = arg

# Order Management
class OrderView(AdminRequiredMixin, ListView):
    """docstring for OrderView"""
    model = Cart
    context_object_name = "list_order"
    template_name = "admin/order_index.html"

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        info = {
            'title': 'Order - Book Review System',
            'sidebar': ['order']
        }
        context['info'] = info
        return context

class OrderDetailView(AdminRequiredMixin, DetailView):
    """docstring for OrderDetailView"""
    model = Cart
    template_name = "admin/order_detail.html"

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        info = {
            'title': 'Order Detail - Book Review System',
            'sidebar': ['order']
        }
        context['info'] = info
        context['list_order_detail'] = Item.objects.filter(cart=self.object)
        return context

class OrderUpdateView(AdminRequiredMixin, UpdateView):
    """docstring for OrderUpdateView"""
    model = Cart
    template_name = "admin/order_update.html"
    form_class = forms.OrderForm

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        info = {
            'title': 'Update Order - Book Review System',
            'sidebar': ['order']
        }
        context['info'] = info
        return context

    def get_success_url(self):
        return reverse_lazy('admin:list_order')

class OrderDeleteView(AdminRequiredMixin, DeleteView):
    """docstring for OrderDeleteView"""
    model = Cart

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin:list_order')