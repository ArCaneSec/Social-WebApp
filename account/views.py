from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm

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
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


def user_login(request) -> HttpResponse:
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
