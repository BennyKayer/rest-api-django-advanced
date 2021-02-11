from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manages user actions

    Args:
        BaseUserManager (BaseUserManager):
        https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager
    """

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user

        Args:
            email (str): User email
            password (string, optional): User's password. Defaults to None.
        """
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        # Manager has access to underlying model
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # good practice, supports multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user

        Args:
            email (str): Superuser's email
            password (str): Superuser's password
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username

    Args:
        AbstractBaseUser (AbstractBaseUser):
        https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser
        PermissionsMixin (PermissionsMixin):
        https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.PermissionsMixin
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
