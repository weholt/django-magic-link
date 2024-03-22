from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    has_verified_email = models.BooleanField(default=False)

    class Meta:
        abstract = True
