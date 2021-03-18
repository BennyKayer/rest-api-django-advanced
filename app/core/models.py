import os
import uuid

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields import CharField


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image

    Args:
        instance ([type]): [description]
        filename ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("uploads/recipe/", filename)


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


class Tag(models.Model):
    """Tag to be used for a recipe

    Args:
        models ([type]): [description]
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe

    Args:
        models ([type]): [description]
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Recipe object

    Args:
        models ([type]): [description]
    """

    ALLERGIES_CODES = (("GL", "Glucose"), ("LT", "Lactose"), ("EG", "Eggs"))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # Will create blank = "" strings in db
    # don't use null if you don't want to chech for 2 values here
    link = models.CharField(max_length=255, blank=True)
    # Could also be passed as class Ingredient
    # but then it would require Ingredient to be above Recipe
    ingredients = models.ManyToManyField("Ingredient")
    tags = models.ManyToManyField("Tag")
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    allergies_codes = ArrayField(
        CharField(
            max_length=5,
            choices=ALLERGIES_CODES,
        ),
        null=True,
    )

    def __str__(self):
        return self.title
