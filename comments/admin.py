from django.contrib import admin
from comments.models import User, Comment, UploadedFile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "homepage")
    search_fields = ("username", "email")
    list_filter = ("username",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "parent")
    search_fields = ("user__username", "text")
    list_filter = ("created_at",)
    ordering = ["-created_at"]
    list_per_page = 25


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ("file", "comment", "uploaded_at")
    search_fields = ("file",)
    list_filter = ("uploaded_at",)
