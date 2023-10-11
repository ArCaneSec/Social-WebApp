import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgest = {
            "url": forms.HiddenInput,
        }

    def clean_url(self):
        url: str = self.cleaned_data["url"]
        valid_extensions: list[str] = ["jpeg", "png", "jpg"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("Extension is not valid")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """
        Downloading the image, saving if commit is True
        """
        image: Image = super().save(commit=False)
        image_url: str = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"
        # download image from the given URL
        response = requests.get(image_url)
        image.image.save(image_name, ContentFile(response.content), save=False)
        if commit:
            image.save()
        return image
