from datetime import datetime
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
from .utils import createAuth0User

class CustomUserManager(BaseUserManager):


    def create_user(self, email, name, password=None,**otherfields):
        """
        Creates and saves a User with the given email and password.
        """
        otherfields.setdefault('is_active',True)
        if not email:
            raise ValueError('Users must have an email address')

        response = createAuth0User(email,password,name)
        data = response.json()
        id = data['_id']
        username = 'auth0.' + id
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            name=name,**otherfields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None,**otherfields):
        """
        Creates and saves a superuser with the given email and password.
        """
        otherfields.setdefault('is_staff',True)
        otherfields.setdefault('is_superuser',True)
        otherfields.setdefault('is_active',True)

        return self.create_user(
            email=username,
            password=password,
            name=name,
            **otherfields
        )


class User(AbstractBaseUser,PermissionsMixin):

    last_login = None

    username = models.CharField(max_length=200,unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    created_on = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()
    
    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'username'