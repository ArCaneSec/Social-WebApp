from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

# app_name = "account"

urlpatterns = [
    # path("login/", views.user_login, name="login_form"),
    path("", views.dashboard, name="dashboard"),

    # Login / Logout urls
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Password reset urls
    path("password-change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("password-change/done", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
]
