from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# Create your views here.


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
