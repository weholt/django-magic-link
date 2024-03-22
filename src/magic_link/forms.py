from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()


class CreateUserForm(ModelForm):

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
