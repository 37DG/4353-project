from django.test import TestCase, Client
from django.urls import reverse
from .models import User
import json

# Create your tests here.
class UserManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(
            email="test@example.com",
            name="Test User",
            role="Basicuser",
            status="1"
        )
        self.client.session["user_email"] = self.test_user.email
        self.client.session.save()

    def test_create_user_success(self):
        response = self.client.post(
            reverse('UserManagement:create_user'),
            data=json.dumps({
                "name": "New User",
                "email": "new@example.com",
                "role": "Basicuser",
                "status": "1"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(email="new@example.com").count(), 1)

    def test_create_user_missing_fields(self):
        response = self.client.post(
            reverse('UserManagement:create_user'),
            data=json.dumps({
                "name": "New User"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_update_user_success(self):
        response = self.client.post(
            reverse('UserManagement:update_user'),
            data=json.dumps({
                "email": self.test_user.email,
                "name": "Updated Name"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.name, "Updated Name")

    def test_update_user_not_found(self):
        response = self.client.post(
            reverse('UserManagement:update_user'),
            data=json.dumps({
                "email": "nonexistent@example.com",
                "name": "Should Fail"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_user_success(self):
        response = self.client.post(
            reverse('UserManagement:delete_user'),
            data=json.dumps({
                "name": self.test_user.name,
                "email": self.test_user.email
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email=self.test_user.email).exists())

    def test_delete_user_admin_block(self):
        self.test_user.role = "Administrator"
        self.test_user.save()

        response = self.client.post(
            reverse('UserManagement:delete_user'),
            data=json.dumps({
                "name": self.test_user.name,
                "email": self.test_user.email
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_change_username_success(self):
        session = self.client.session
        session["user_email"] = self.test_user.email
        session.save()

        response = self.client.post(
            reverse('UserManagement:changeUsername'),
            data=json.dumps({
                "name": "Changed Name"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.name, "Changed Name")


    def test_change_username_missing(self):
        response = self.client.post(
            reverse('UserManagement:changeUsername'),
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)