from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ImageCreateForm
from .models import Image

# Create your views here.


@login_required
def create_image(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            _ = form.cleaned_data
            new_image: Image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Image added succesfully.")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(
        request,
        "images/image/create.html",
        {"section": "images", "form": form},
    )
