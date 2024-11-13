from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
import re


class User(models.Model):
    username = models.CharField(
        max_length=100, unique=True, validators=[MinLengthValidator(1)]
    )
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    homepage = models.URLField(blank=True, default="")
    captcha = models.CharField(
        max_length=6, validators=[MinLengthValidator(6)], blank=True
    )

    def __str__(self):
        return self.username


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    text = models.TextField(validators=[MinLengthValidator(1)], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if isinstance(self.text, str) and self.text:
            allowed_tags = ["a", "code", "i", "strong"]
            pattern = r"<(?!/?(?:" + "|".join(allowed_tags) + r")\b)[^>]*>"
            self.text = re.sub(pattern, "", self.text)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        user = getattr(self.user, "username", "Unknown User")
        return f"Comment by {user} at {self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    comment = models.ForeignKey(Comment, related_name="files", on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        file_name = self.file.name if self.file else "No File"
        comment_id = getattr(self.comment, "id", "No Comment")
        return f"File {file_name} for comment {comment_id}"
