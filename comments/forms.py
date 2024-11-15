from django import forms
from django.core.exceptions import ValidationError
from .models import Comment
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ["username", "email", "homepage", "text", "captcha"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.isalnum():  # Перевірка на латинські літери та цифри
            raise ValidationError("Username can only contain letters and numbers.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if "@" not in email:
            raise ValidationError("Enter a valid email address.")
        return email
