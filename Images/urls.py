from django.urls import path

from . import views

app_name = "images"

urlpatterns = [
    path("", views.image_list, name="list"),
    path("create/", views.create_image, name="create"),
    path("like/", views.image_like, name="like"),
    path("detail/<int:id>/<slug:slug>/", views.image_details, name="detail"),
]
