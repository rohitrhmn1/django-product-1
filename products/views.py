from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from accounts.models import User
from products.forms import ProductForm
from products.models import Product


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Product.objects.all()


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/productDetail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class ProductDetailsUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/productEdit.html'
    form_class = ProductForm
    slug_field = 'id'
    slug_url_kwarg = 'id'


class ProductAddView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/productForm.html'

    success_url = reverse_lazy('products:index')

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return self.success_url

    def form_valid(self, form):
        product = form.save(commit=False)
        product.added_by = User.objects.get(id=self.request.user.id)  # use your own profile here
        product.current = True
        product.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/productDeleteConfirm.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    success_url = reverse_lazy('products:index')

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return self.success_url
