from django.urls import reverse
from typing import Optional
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

User = get_user_model()


def send_sign_in_email(request: HttpRequest, user: User) -> None:
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = request.build_absolute_uri(reverse('magic-link:verify-email', args=[uid, token])) #f"{os.environ['EMAIL_VERIFICATION_URL']}/{uid}/{token}/"

    subject = "Verify your email address 🚀"
    message = "Hi there 🙂\n" "Please click " f'<a href="{verification_link}" target="_blank">here</a> ' "to verify your email address"
    send_mail(subject, "", settings.EMAIL_HOST_USER, [user.email], html_message=message)


def decode_uid(uidb64: str) -> Optional[str]:
    """Decode the base64 encoded UID."""
    try:
        return urlsafe_base64_decode(uidb64).decode()
    except (TypeError, ValueError, OverflowError) as e:
        print(f"Error decoding uid: {e}")
        return None


def get_user_by_uid(uid: str) -> Optional[User]:
    """Retrieve user object using UID."""
    try:
        return User.objects.get(pk=uid)
    except User.DoesNotExist as e:
        print(f"Error getting user from uid: {e}")
        return None
