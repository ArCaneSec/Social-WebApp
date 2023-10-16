from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.


class CustomUser(AbstractUser):
    """
    Extending user model, adding birthdate, photo field.
    """

    birthdate = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)
    following = models.ManyToManyField(
        "self", through="Contact", related_name="followers", symmetrical=False
    )

    def __str__(self) -> str:
        return f"Profile of {super().username}"

    def get_absolute_url(self):
        return reverse("user_detail", args=[self.username])


class Contact(models.Model):
    user_from = models.ForeignKey(
        CustomUser, related_name="rel_from_set", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        CustomUser, related_name="rel_to_set", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"{self.user_from} has followed {self.user_to}"
