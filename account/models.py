from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    """
    Extending user model, adding birthdate, photo field.
    """

    birthdate = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self) -> str:
        return f"Profile of {super().username}"
