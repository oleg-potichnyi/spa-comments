from django.test import TestCase
from django.core.exceptions import ValidationError
from comments.models import User, Comment, UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            homepage="https://example.com",
            captcha="123456",
        )

    def test_create_user(self):
        """
        Test creating a user and checking its attributes.
        """
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.homepage, "https://example.com")

    def test_username_min_length(self):
        """
        Test that a user with an empty username raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            user = User(username="", email="fail@example.com")
            user.full_clean()

    def test_email_validation(self):
        """
        Test that an invalid email format raises a ValidationError.
        """
        with self.assertRaises(ValidationError):
            user = User(username="user2", email="not-an-email")
            user.full_clean()

    def test_str_method(self):
        """
        Test the string representation of a user.
        """
        self.assertEqual(str(self.user), "testuser")


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser2", email="user2@example.com"
        )
        self.comment = Comment.objects.create(
            user=self.user, text="This is a test comment"
        )

    def test_create_comment(self):
        """
        Test creating a comment and checking its attributes.
        """
        comment_count = Comment.objects.count()
        self.assertEqual(comment_count, 1)
        self.assertEqual(self.comment.text, "This is a test comment")
        self.assertEqual(self.comment.user.username, "testuser2")

    def test_comment_with_parent(self):
        """
        Test creating a reply to a comment and
        checking parent-child relationship.
        """
        reply = Comment.objects.create(
            user=self.user, parent=self.comment, text="This is a reply"
        )
        self.assertEqual(reply.parent, self.comment)
        self.assertEqual(reply.parent.text, "This is a test comment")

    def test_str_method(self):
        """
        Test the string representation of a comment.
        """
        self.assertIn("Comment by testuser2", str(self.comment))


class UploadedFileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser3", email="user3@example.com"
        )
        self.comment = Comment.objects.create(
            user=self.user, text="Another comment"
        )
        self.uploaded_file = UploadedFile.objects.create(
            file=SimpleUploadedFile("test.txt", b"file content"),
            comment=self.comment,
        )

    def test_create_uploaded_file(self):
        """
        Test creating an uploaded file and checking its attributes.
        """
        file_count = UploadedFile.objects.count()
        self.assertEqual(file_count, 1)
        self.assertEqual(self.uploaded_file.comment, self.comment)
