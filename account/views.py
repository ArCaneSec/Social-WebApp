from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from actions.models import Action
from actions.utils import create_action

from .forms import EditProfile, LoginForm, UserRegistrationForm
from .models import Contact, CustomUser

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
            create_action(new_user, "has created an account")
            return render(
                request, "account/register_done.html", {"new_user": new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


def user_login(request):
    """
    Login Form, simple get requests will receive raw form to login.
    Post requests will initiate an authentication method
    against provided credentials.
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
    """Home page"""
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list("id", flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related("user").prefetch_related("target")[:10]
    return render(
        request,
        "account/dashboard.html",
        {"section": "dashboard", "actions": actions},
    )


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
    """Returning active users in platform"""
    users = CustomUser.objects.filter(is_active=True)
    return render(
        request,
        "account/user/list.html",
        {"section": "people", "users": users},
    )


@login_required
def user_detail(request, username):
    """Retriving a specific user details."""
    user = get_object_or_404(CustomUser, username=username, is_active=True)
    return render(
        request,
        "account/user/detail.html",
        {"section": "people", "user": user},
    )


@require_POST
@login_required
def user_follow(request):
    """
    This view is responsible for follow and unfollow action.
    """
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if not user_id and action:
        return JsonResponse(
            {
                "status": "error",
                "message": "action and user_id parameters must specified",
            },
            status=400,
        )
    try:
        user = CustomUser.objects.get(id=user_id)
        if user == request.user:
            return JsonResponse(
                {"status": "error", "message": "Invalid user"}, status=400
            )
        if action == "follow":
            Contact.objects.get_or_create(user_from=request.user, user_to=user)
            create_action(request.user, "is following", user)

        else:
            Contact.objects.filter(
                user_from=request.user, user_to=user
            ).delete()
            create_action(request.user, "has unfollowed", user)
        return JsonResponse({"status": "ok"})
    except CustomUser.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "user not found"}, status=404
        )
