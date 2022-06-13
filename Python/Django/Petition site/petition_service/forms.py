from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category


class SignUpForm(UserCreationForm):
    last_name = forms.CharField(label='Прізвище', max_length=30)
    first_name = forms.CharField(label='Ім\'я', max_length=30)
    email = forms.EmailField(label='Електронна пошта', max_length=254)

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email', 'username', 'password1', 'password2', )

class LoginForm(forms.Form):
    username = forms.CharField(label='Ім\'я користувача')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class CreationForm(forms.Form):
    category = forms.ModelChoiceField(label='Категорія', queryset=Category.objects.all())
    title = forms.CharField(label='Заголовок', max_length=100)
    text = forms.CharField(label="Зміст", widget=forms.Textarea)

class SearchForm(forms.Form):
    field = forms.CharField(label='user', max_length=150)
    choices = (('1', "користувачем"),
               ('2', "назвою петиції"),
               ('3', "вмістом петиції"))
    select = forms.ChoiceField(label='Пошук за', choices=choices)