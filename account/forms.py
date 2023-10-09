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
    password_repeat = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name"]

    def clean_password_repeat(self):
        data = self.cleaned_data
        if data["password"] != data["password_repeat"]:
            raise forms.ValidationError("Passwords don't match.")
        return data["password"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use.")
        return data


class EditProfile(forms.ModelForm):
    """
    This form is to let users edit their profile.
    They are allowed to change their FIELDS data.
    """

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "photo"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = CustomUser.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email already in use.")
        return data
