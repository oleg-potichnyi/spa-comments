from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Comment, UploadedFile
import json


@csrf_exempt
def user_list(request):
    if request.method == "GET":
        users = list(
            User.objects.values("id", "username", "email", "homepage")
        )
        return JsonResponse(users, safe=False)
    return HttpResponse(status=405)


@csrf_exempt
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    if request.method == "GET":
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "homepage": user.homepage,
        }
        return JsonResponse(user_data)
    return HttpResponse(status=405)


@csrf_exempt
def comment_list(request):
    if request.method == "GET":
        comments = list(
            Comment.objects.values(
                "id", "user__username", "text", "created_at", "parent_id"
            )
        )
        return JsonResponse(comments, safe=False)
    return HttpResponse(status=405)


@csrf_exempt
def comment_detail(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Comment not found"}, status=404)

    if request.method == "GET":
        comment_data = {
            "id": comment.id,
            "user": comment.user.username,
            "text": comment.text,
            "created_at": comment.created_at,
            "parent_id": comment.parent_id,
        }
        return JsonResponse(comment_data)
    return HttpResponse(status=405)


@csrf_exempt
def reply_to_comment(request, id):
    try:
        parent_comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return JsonResponse({"error": "Parent comment not found"}, status=404)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        user_id = data.get("user_id")
        text = data.get("text")

        if not user_id or not text:
            return JsonResponse(
                {"error": "User ID and text are required"}, status=400
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        reply = Comment.objects.create(
            user=user, parent=parent_comment, text=text
        )
        return JsonResponse(
            {"id": reply.id, "text": reply.text, "user": reply.user.username},
            status=201,
        )
    return HttpResponse(status=405)


@csrf_exempt
def uploaded_file_list(request):
    if request.method == "GET":
        files = list(
            UploadedFile.objects.values(
                "id", "file", "uploaded_at", "comment_id"
            )
        )
        return JsonResponse(files, safe=False)
    return HttpResponse(status=405)


@csrf_exempt
def uploaded_file_detail(request, id):
    try:
        uploaded_file = UploadedFile.objects.get(id=id)
    except UploadedFile.DoesNotExist:
        return JsonResponse({"error": "File not found"}, status=404)

    if request.method == "GET":
        file_data = {
            "id": uploaded_file.id,
            "file": uploaded_file.file.url,
            "uploaded_at": uploaded_file.uploaded_at,
            "comment_id": uploaded_file.comment_id,
        }
        return JsonResponse(file_data)
    return HttpResponse(status=405)
