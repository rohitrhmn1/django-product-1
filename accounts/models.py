from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField
from internship import utils

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

AUTH_PROVIDERS = {
    'facebook': 'facebook',
    'google': 'google',
    'twitter': 'twitter',
    'email': 'email',
}


class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD + '__iexact': email})

    def create_user(self, email, password):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password must be provided')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, ):
    unique_id = models.CharField(max_length=50, default=utils.unique_id_generator, unique=True)
    name = models.CharField(max_length=255, null=False, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = PhoneNumberField()
    username = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=1)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False, help_text="verified status")
    is_admin = models.BooleanField(default=False, help_text="Admin status")
    is_active = models.BooleanField(default=True, help_text="Active status")
    is_staff = models.BooleanField(default=False, help_text="Staff status")
    is_superuser = models.BooleanField(default=False, help_text="Superuser status")
    profile_img = models.ImageField(upload_to=utils.user_image_upload_path, blank=True, null=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, package_name):
        return True

    def get_absolute_url(self):
        return reverse('auth:details', kwargs={'unique_id': self.unique_id})
