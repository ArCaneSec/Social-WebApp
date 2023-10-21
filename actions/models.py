from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Action(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="actions", on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["-created"])]
        ordering = ["-created"]
