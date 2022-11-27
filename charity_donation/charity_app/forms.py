from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Institution, Donation
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import EmailValidator, URLValidator

User = get_user_model()


class RegisterUserForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(max_length=50,
                              widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(min_length=4, max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(min_length=4, max_length=20,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean_email(self):
        cd = super().clean()
        email = cd.get('email')
        if User.objects.filter(username=email).exists():
            raise ValidationError('Użytkownik z takim mailem już istnieje!')
        return email

    def clean_password2(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 != password2:
            raise ValidationError('Hasla nie są identyczne!')
        return password2


class LoginUserForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(min_length=4, max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean_password(self):
        cd = super().clean()
        username = cd.get('email')
        password = cd.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('Dane logowania nie są prawidłowe!')
        return password


# class DonationForm(forms.ModelForm):
#     class Meta:
#         model = Donation
#         fields = '__all__'


class DonationForm(forms.Form):
    quantity = forms.IntegerField()
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    institution = forms.CharField()
    address = forms.CharField()
    phone_number = forms.IntegerField()
    city = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=6)
    pick_up_date = forms.DateField()
    pick_up_time = forms.TimeField()
    pick_up_comment = forms.CharField()
    user = forms.ModelChoiceField(queryset=User.objects.all())
