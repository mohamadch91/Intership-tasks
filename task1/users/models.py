from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None, **extra_fields):
        if not phone:
            raise ValueError("The phone number must be set.")
        user = self.model(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, first_name, last_name, password=None, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["role"] = "administration"
        return self.create_user(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields,
        )

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        CLIENT = "client"
        ADMINISTRATION = "administration"
        AUTHOR = "author"
    
    phone = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()