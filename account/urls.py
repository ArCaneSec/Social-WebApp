from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

# app_name = "account"

urlpatterns = [
    # The paths below are incase that you dont want to use django.contrib.auth.urls urls
    
    #  path("login/", views.user_login, name="login_form"),
    ## Login / Logout urls
    #path("login/", auth_views.LoginView.as_view(), name="login"),
    #path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    ## Password change urls
    #path("password-change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    #path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    ## Password reset urls
    #path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    #path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    #path("password-reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    #path("password-reset/complete", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path("", views.dashboard, name="dashboard"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("edit/", views.edit_profile, name="edit"),
]
