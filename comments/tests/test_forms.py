from django import forms
from django.core.exceptions import ValidationError
from comments.models import Comment
from captcha.fields import CaptchaField
import re


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ["user", "text", "captcha"]

    def clean_username(self):
        """
        Ensure the username contains only alphanumeric characters.
        """
        username = self.cleaned_data.get("user").username
        if not username.isalnum():
            raise ValidationError(
                "Username can only contain letters and numbers."
            )
        return username

    def clean_email(self):
        """
        Ensure the email contains a valid '@' symbol.
        """
        email = self.cleaned_data.get("user").email
        if "@" not in email:
            raise ValidationError("Enter a valid email address.")
        return email

    def clean_homepage(self):
        """
        Ensure the homepage is a valid URL.
        """
        homepage = self.cleaned_data.get("user").homepage
        if homepage and not re.match(
            r"^(https?://)?[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+$", homepage
        ):
            raise ValidationError("Enter a valid URL.")
        return homepage

    def clean_text(self):
        """
        Remove any disallowed HTML tags from the comment text.
        """
        text = self.cleaned_data.get("text")
        if text:
            allowed_tags = ["a", "code", "i", "strong"]
            pattern = r"<(?!/?(?:" + "|".join(allowed_tags) + r")\b)[^>]*>"
            text = re.sub(pattern, "", text)
        return text
