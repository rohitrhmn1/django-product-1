from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import UserUpdateProfileForm, UserLoginAuthenticationForm, UserRegistrationForm
from accounts.models import User
from products.models import Product


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/userRegister.html'

    def form_valid(self, form):
        valid = super(UserRegisterView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(self.request, username=email, password=password)
        login(self.request, new_user)
        return valid


class UserInformationView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/userDetails.html'
    slug_field = 'unique_id'
    slug_url_kwarg = 'unique_id'

    def get_context_data(self, **kwargs):
        context = super(UserInformationView, self).get_context_data(**kwargs)
        if context.get('user') == self.request.user:
            context['products'] = Product.objects.filter(added_by=self.request.user)
            return context
        return {}


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateProfileForm
    template_name = 'accounts/userUpdateForm.html'
    slug_field = 'unique_id'
    slug_url_kwarg = 'unique_id'


class UserLoginView(LoginView):
    form_class = UserLoginAuthenticationForm
    template_name = 'accounts/userLogin.html'


def logout_view(request):
    logout(request)
    return render(request, 'accounts/userLogout.html')
