from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Institution, Donation
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import EmailValidator, URLValidator

User = get_user_model()


class RegisterUserForm(forms.Form):
    name = forms.CharField(label='Imię', max_length=30)
    surname = forms.CharField(label='Nazwisko', max_length=50)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    # class Meta:
    #     model = User
    #     fields = [
    #         'name',
    #         'surname',
    #         'email',
    #         'password1',
    #         'password2',
    #     ]

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(username=email).exists():
    #         raise ValidationError('Użytkownik z takim mailem już istnieje!')
    #     return email
    #
    # def clean_password2(self):
    #     # cd = super().clean()
    #     # password1 = cd.get('password1')
    #     # password2 = cd.get('password2')
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']
    #     if password1 != password2:
    #         raise ValidationError('Hasla nie są identyczne!')
    #     return password2


class LoginUserForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
