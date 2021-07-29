from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                   "this user's password, but you can change the password "
                   "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = (
            'name',
            'profile_img',
            'email',
            'phone',
            'username',
            'password',
            'gender',
            'date_of_birth',
            'is_active',
            'is_admin',
            'is_staff',
        )


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        'email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff',
    )
    fieldsets = (
        ('Contact Details', {'fields': ('email', 'username', 'phone',)}),
        ('Password', {'fields': ('password',)}),
        ('Personal info', {'fields': ('name', 'gender', 'date_of_birth', 'profile_img',)}),
        ('Access Level', {'fields': ('is_verified', 'is_active', 'is_admin', 'is_staff', 'is_superuser',)}),
        ('System Data', {'fields': ('id', 'date_joined', 'last_login', 'unique_id', 'auth_provider',)}),

    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2'), }),
    )
    list_filter = ('is_admin', 'is_staff', 'is_active',)
    search_fields = ('email', 'username', 'phone',)
    readonly_fields = ('id', 'date_joined', 'last_login', 'unique_id', 'auth_provider',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
