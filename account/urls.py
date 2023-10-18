from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = "account"

urlpatterns = [
    # The paths below are incase that you dont want to use django.contrib.auth.urls urls
    #  path("login/", views.user_login, name="login_form"),
    ## Login / Logout urls
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    ## Password change urls
    # path("password-change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    # path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    ## Password reset urls
    # path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    # path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path("password-reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path("password-reset/complete", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit_profile, name="edit"),
    path("users/", views.users_list, name="user_list"),
    path("users/follow/", views.user_follow, name="user_follow"),
    path("users/<username>/", views.user_detail, name="user_detail"),
]
