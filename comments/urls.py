from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.user_list, name="user_list"),
    path("users/<int:id>/", views.user_detail, name="user_detail"),
    path("comments/", views.comment_list, name="comment_list"),
    path("comments/<int:id>/", views.comment_detail, name="comment_detail"),
    path(
        "comments/<int:id>/reply/",
        views.reply_to_comment,
        name="reply_to_comment"
    ),
    path("files/", views.uploaded_file_list, name="uploaded_file_list"),
    path(
        "files/<int:id>/",
        views.uploaded_file_detail,
        name="uploaded_file_detail"
    ),
]
