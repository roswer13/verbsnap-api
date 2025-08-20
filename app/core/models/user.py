"""
User model.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """ Manager for users. """

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """Create and return a superuser with given email and password."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(
        verbose_name=_('Email'), max_length=128, unique=True,
        help_text=_('Email address of the user.')
    )
    name = models.CharField(
        verbose_name=_('User name'), max_length=128,
        help_text=_('Name of the user.')
    )
    is_staff = models.BooleanField(
        verbose_name=_('Staff'), default=False,
        help_text=_('Is a user of the internal equipment.'),
    )
    is_active = models.BooleanField(
        verbose_name=_('Active'), default=True,
        help_text=_('Indicates if the user is active.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """Return string representation of user."""
        return self.email
