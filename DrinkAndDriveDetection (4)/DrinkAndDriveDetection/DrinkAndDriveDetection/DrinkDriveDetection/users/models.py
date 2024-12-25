from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class ClientRegisterManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class Gender(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class ClientRegister_Model(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phoneno = models.CharField(max_length=15)  # Ensure this field is correctly defined
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Manager to handle user creation logic
    objects = ClientRegisterManager()

    # Make `email` the unique identifier for authentication
    USERNAME_FIELD = 'email'

    # These fields must be provided when creating a superuser
    REQUIRED_FIELDS = ['username', 'phoneno']

    def __str__(self):
        return self.email

    # Optionally, add methods for saving or custom behaviors if needed
    def save(self, *args, **kwargs):
        if not self.phoneno:
            raise ValueError('Phone number must be provided')
        super().save(*args, **kwargs)
