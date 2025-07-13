from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Неверное имя пользователя или пароль.")
            # Сохраняем пользователя в форме для последующего использования во вью
            self.user_cache = user
        return cleaned_data