# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from captcha.fields import CaptchaField
from models import Settings, Article
from django import forms


class AuthForm(AuthenticationForm):
    username = forms.CharField(label="Nom utilisateur", max_length=30,
                               widget=forms.TextInput(attrs={'placeholder': "nom d'utilisateur", 'data-mini': 'true', 'required': 'true'}))
    password = forms.CharField(label="Mot de passe", min_length=8,
                               widget=forms.PasswordInput(attrs={'placeholder': "mot de passe", 'data-mini': 'true', 'required': 'true'}))

    def check_for_test_cookie(self):
        pass


class AuthFormWithCaptcha(AuthForm):
    captcha = CaptchaField(label="Test de Turing")


class ProfileForm(PasswordChangeForm):
    new_password1 = forms.CharField(label="Nouveau mot de passe", min_length=8, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmation du nouveau mot de passe", min_length=8, widget=forms.PasswordInput)


class SubscribeForm(UserCreationForm):
    password1 = forms.CharField(label="Mot de passe", min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation du mot de passe", min_length=8, widget=forms.PasswordInput)
    captcha = CaptchaField(label="Test de Turing")


class SettingsForm(forms.ModelForm):

    class Meta:
        model = Settings


class CreateArticleForm(forms.ModelForm):
    text = forms.CharField(label="Contenu de l'article", widget=forms.Textarea)

    class Meta:
        model = Article
        exclude = ['state',]


class EditArticleForm(forms.ModelForm):
    text = forms.CharField(label="Contenu de l'article", widget=forms.Textarea)

    class Meta:
        model = Article
        exclude = ['title', 'state', 'wiki']

