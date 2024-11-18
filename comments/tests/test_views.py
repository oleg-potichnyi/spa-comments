from django.test import TestCase, Client
from django.urls import reverse
from comments.models import User, Comment, UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile
import json


class UserViewTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username="testuser1", email="user1@example.com"
        )
        self.user2 = User.objects.create(
            username="testuser2", email="user2@example.com"
        )
        self.client = Client()

    def test_user_list_get(self):
        """
        Test retrieving the list of users.
        """
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_user_detail_get(self):
        """
        Test retrieving details of a specific user.
        """
        response = self.client.get(
            reverse("user_detail", args=[self.user1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "testuser1")

    def test_user_detail_not_found(self):
        """
        Test retrieving a user that does not exist.
        """
        response = self.client.get(reverse("user_detail", args=[999]))
        self.assertEqual(response.status_code, 404)


class CommentViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="commenter", email="commenter@example.com"
        )
        self.comment1 = Comment.objects.create(
            user=self.user, text="First comment"
        )
        self.comment2 = Comment.objects.create(
            user=self.user, text="Second comment", parent=self.comment1
        )
        self.client = Client()

    def test_comment_list_get(self):
        """
        Test retrieving the list of comments.
        """
        response = self.client.get(reverse("comment_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_comment_detail_get(self):
        """
        Test retrieving details of a specific comment.
        """
        response = self.client.get(
            reverse("comment_detail", args=[self.comment1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "First comment")

    def test_comment_detail_not_found(self):
        """
        Test retrieving a comment that does not exist.
        """
        response = self.client.get(reverse("comment_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_reply_to_comment(self):
        """
        Test replying to an existing comment.
        """
        data = {"user_id": self.user.id, "text": "Reply to comment"}
        response = self.client.post(
            reverse("reply_to_comment", args=[self.comment1.id]),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["text"], "Reply to comment")


class UploadedFileViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="uploader", email="uploader@example.com"
        )
        self.comment = Comment.objects.create(
            user=self.user, text="Comment for file"
        )
        self.uploaded_file = UploadedFile.objects.create(
            file=SimpleUploadedFile("test.txt", b"Hello World"),
            comment=self.comment
        )
        self.client = Client()

    def test_uploaded_file_list_get(self):
        """
        Test retrieving the list of uploaded files.
        """
        response = self.client.get(reverse("uploaded_file_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_uploaded_file_detail_not_found(self):
        """
        Test retrieving a non-existing uploaded file.
        """
        response = self.client.get(reverse("uploaded_file_detail", args=[999]))
        self.assertEqual(response.status_code, 404)
