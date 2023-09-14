from django import forms
from .models import CustomUser


class LoginForm(forms.Form):
    """
    Login form to let users sign in
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """
    User registration form to let users sign up via their email and username
    """

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name"]

    def clean_password_repeat(self):
        data = self.cleaned_data
        if data["password"] != data["password_repeat"]:
            raise forms.ValidationError("Passwords don't match.")
        return data["password"]
