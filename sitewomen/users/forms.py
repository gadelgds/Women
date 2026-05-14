from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-input"})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Email уже используется!")
        return email

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "photo", "date_birth"]
        widgets = {
            "date_birth": forms.SelectDateWidget(years=range(datetime.date.today().year - 100, datetime.date.today().year + 1))
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].disabled = True
        self.fields["email"].disabled = True
        for field in self.fields:
            if field != "date_birth":
                self.fields[field].widget.attrs.update({"class": "form-input"})

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-input"})
