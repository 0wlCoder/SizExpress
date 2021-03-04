from django.contrib import admin
from django.urls import path
from django.views.generic.base import View
from .views import main_view, signup_view
from profiles.views import my_recommendations_view
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import ActivateAccount

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main_view, name="home"),
    path("signup/", signup_view, name="register"),
    path("profiles/", my_recommendations_view, name="my-recs-view"),
    path("login/", views.loginPage, name="login"),
    path("login/login", views.loginPage, name="login"),
    path("rates/", views.rates, name="rates"),
    path("profileinfo/", views.profileInfo, name="profileinfo"),
    path("logout/", views.logoutPage, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("Affiliate_account/", views.Affiliate_account, name="Affiliate_account"),
    path("Bank_Update/", views.Bank_account_update, name="Bank_Update"),
    path("withdrawalmail/", views.withdrawalmail, name="withdrawalmail"),
    # path("resendemail/", views.resendmail, name="resend_mail"),
    # path(
    #     "login/resendmail/",
    #     views.resendmail,
    #     name="resend_mail",
    # ),
    path("activate/<uidb64>/<token>/", ActivateAccount.as_view(), name="activate"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="reset_password_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="reset_password_done.html"
        ),
        name="password_reset_complete",
    ),
    path("<str:ref_code>/", main_view, name="home"),
]