from django.urls import path

from . import views

app_name = "magic-link"

urlpatterns = [
    path("", views.home, name="home"),
    path("sign-in", views.SendSignInEmail.as_view(), name="sign-in"),
    path("sign-out", views.sign_out, name="sign-out"),
    path("verify-email/<uidb64>/<token>/", views.verify_email, name="verify-email"),
]
