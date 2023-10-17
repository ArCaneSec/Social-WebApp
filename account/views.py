from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import EditProfile, LoginForm, UserRegistrationForm
from .models import CustomUser

# Create your views here.


def register(request):
    """
    This view will handle the user sign up functionality.
    Rendering different templates based on the request method.
    """

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(
                request, "account/register_done.html", {"new_user": new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


def user_login(request):
    """
    Login Form, simple get requests will receive raw form to login,
    while post requests will initiate an authentication method against provided credentials.
    """

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated Succesfully")
                else:
                    return HttpResponse("Your account is disabled!")
            else:
                return HttpResponse("Invalid Credentials")
    else:
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


@login_required
def edit_profile(request):
    """
    This view is to let users edit their profile.
    The client MUST be authenticated to access this view.
    """
    if request.method == "POST":
        user_form = EditProfile(
            instance=request.user, data=request.POST, files=request.FILES
        )
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile Updated")
        else:
            messages.error(request, "Error while updating your profile!")

    else:
        user_form = EditProfile(instance=request.user)

    return render(request, "account/edit.html", {"user_form": user_form})


@login_required
def users_list(request):
    users = CustomUser.objects.filter(is_active=True)
    return render(
        request,
        "account/user/list.html",
        {"section": "people", "users": users},
    )


@login_required
def user_detail(request, username):
    user = get_object_or_404(CustomUser, username=username, is_active=True)
    return render(
        request,
        "account/user/detail.html",
        {"section": "people", "user": user},
    )
