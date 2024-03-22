from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import CreateUserForm, ProfileForm
from .services import decode_uid, get_user_by_uid, send_sign_in_email

User = get_user_model()


def verify_email(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    """
    Verify user email after the user clicks on the email link.
    """
    uid = decode_uid(uidb64)
    user = get_user_by_uid(uid) if uid else None

    if user and default_token_generator.check_token(user, token):
        user.has_verified_email = True
        user.save()
        login(request, user)
        return redirect("magic-link:home")

    print("Email verification failed")
    return redirect("magic-link:sign-in")


class SendSignInEmail(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_anonymous and request.user.has_verified_email:
            return redirect("magic-link:home")
        form = CreateUserForm()
        return render(request, "magic_link/sign_in.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        data = {"username": request.POST["email"], "email": request.POST["email"], "password": request.POST["email"]}
        user, created = User.objects.get_or_create(email=data["email"], defaults={"username": data["email"], "password": data["email"]})
        return self._send_verification_and_respond(request, user)

    @staticmethod
    def _send_verification_and_respond(request: HttpRequest, user: User) -> HttpResponse:
        send_sign_in_email(request, user)
        message = f"We've sent an email ✉️ to " f'<a href=mailto:{user.email}" target="_blank">{user.email}</a> ' "Please check your email to verify your account"
        return HttpResponse(message)


def sign_out(request: HttpRequest) -> HttpResponse:
    request.session.flush()
    return redirect("magic-link:sign-in")


def home(request: HttpRequest) -> HttpResponse:
    if not request.user.is_anonymous and request.user.has_verified_email:
        form = request.POST and ProfileForm(request.POST, instance=request.user) or ProfileForm(instance=request.user)
        if request.POST and form.is_valid():
            form.save()
        return render(request, "magic_link/home.html", {'profile_form': form})

    return redirect("magic-link:sign-in")
