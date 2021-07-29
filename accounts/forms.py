from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from accounts.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255)
    username = forms.CharField(max_length=50)
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('name', 'email', 'username', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            User.objects.get(email=email)
        except Exception:
            return email
        raise forms.ValidationError(f"Email {email} already in use.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except Exception:
            return username
        raise forms.ValidationError(f" Username {username} taken.")


class UserLoginForm(forms.Form):
    email_id = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


class UserLoginAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput())


class UserUpdateProfileForm(forms.ModelForm):
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='IN'))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    username = forms.CharField(max_length=50, disabled=True)
    name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = [
            'profile_img',
            'username',
            'name',
            'gender',
            'date_of_birth',
            'email',
            'phone',
        ]

        localized_fields = '__all__'
