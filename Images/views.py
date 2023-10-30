import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from actions.utils import create_action

from .forms import ImageCreateForm
from .models import Image

# Create your views here.

r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@login_required
def create_image(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            _ = form.cleaned_data
            new_image: Image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, "bookmarked image", new_image)
            messages.success(request, "Image added succesfully.")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(
        request,
        "images/image/create.html",
        {"section": "images", "form": form},
    )


def image_details(request, id, slug):
    """Responsible for returning details of an image
    increasing its view count as well."""
    image = get_object_or_404(Image, id=id, slug=slug)
    # Increasing total views in redis db
    total_views = r.incr(f"image:{image.id}:views")
    r.zincrby("image_ranking", 1, image.id)
    return render(
        request,
        "images/image/detail.html",
        {"section": "images", "images": image, "total_views": total_views},
    )


@login_required
def image_rankings(request):
    """Returning top 10 of most viewed images on app."""
    image_ranking = r.zrange("image_ranking", 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(
        request,
        "images/image/ranking.html",
        {"section": "images", "most_viewed": most_viewed},
    )


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image: Image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "like", image)
            else:
                image.users_like.remove(request.user)

            return JsonResponse({"status": "OK"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "ERROR"})


@login_required
def image_list(request):
    """
    This view is responsible for listing images with pagination.
    can be called with ajax too.
    """
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get("page")

    # If set, rendering images only instead of whole page
    image_only = request.GET.get("images_only")
    try:
        paginator.page(page)
    except PageNotAnInteger:
        paginator.page(1)
    except EmptyPage:
        if image_only:
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if image_only:
        return render(
            request,
            "images/image/list_images.html",
            {"section": "image", "images": images},
        )
    return render(
        request,
        "images/image/list.html",
        {"section": "image", "images": images},
    )
