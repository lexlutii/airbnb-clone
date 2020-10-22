from django.contrib.auth.models import AbstractUser

from django.db import models

# Create your models here.


class User(AbstractUser):
    """ Custom User Model """
    GENDER_MALE = "ml"
    GENDER_FEMALE = "fml"
    GENDER_UNSPECIFIED = "usp"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_UNSPECIFIED, "Uncpecified")
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_RUSSIAN = "ru"
    LANGUIGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_RUSSIAN, "Russian")
    )

    CURRENCY_USD = "usd"
    CURRENCY_RUB = "rub"
    CURRENCY_CHOICES = ((CURRENCY_USD, "USD"), (CURRENCY_RUB, "RUB"))

    avatar = models.ImageField(blank=True)

    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=3, blank=True)

    bio = models.TextField(blank=True)

    birthday = models.DateField(null=True, blank=True)

    language = models.CharField(
        choices=GENDER_CHOICES, max_length=2, blank=True)

    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True)

    superhost = models.BooleanField(default=False)
