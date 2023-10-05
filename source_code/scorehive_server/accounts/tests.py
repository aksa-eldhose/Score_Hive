from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from score.tests import generate_random_password

from .models import User

passwd = generate_random_password()
email1 = "test@mail.com"
email2 = "test2@mail.com"


# Create your tests here.
class RegisterTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email=email1, password=passwd)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_register_email_data(self):
        response = self.client.post(
            reverse("test"),
            {
                "email": email2,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        response_1 = self.client.post(
            reverse("test"),
            {
                "email": email1,
            },
            format="json",
        )
        self.assertEqual(response_1.status_code, 409)
        response_2 = self.client.post(
            reverse("test"),
            {
                "email": "",
            },
            format="json",
        )
        self.assertEqual(response_2.status_code, 400)

    def test_register_token(self):
        response = self.client.post(
            reverse("emailTokenVerification"),
            {
                "token": "dsjsjhkjhskd.kjfhds.sljsfff",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        response_1 = self.client.post(
            reverse("emailTokenVerification"),
            {},
            format="json",
        )
        self.assertEqual(response_1.status_code, 400)

    def test_register_details(self):
        response = self.client.post(
            reverse("userDetailsSubmission"),
            {
                "token": "dsjsjhkjhskd.kjfhds.sljsffkf",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 422)
        response = self.client.post(
            reverse("userDetailsSubmission"),
            {
                "token": "dsjsjhkjhskd.kjfhds.sljsffkf",
                "name": "asd",
                "phone_number": "1234567890",
                "password": generate_random_password(),
                "confirm_password": generate_random_password(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 422)

    def test_login(self):
        response = self.client.post(
            reverse("userLogin"),
            {
                "email": email1,
                "password": generate_random_password(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            reverse("userLogin"),
            {
                "email": email1,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            reverse("userLogin"),
            {
                "email": email2,
                "password": generate_random_password(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_reset_password(self):
        response = self.client.post(
            reverse("passwordReset"),
            {
                "email": email2,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_reset_token_verify(self):
        response = self.client.post(
            reverse("PasswordResetTokenVerify"),
            {"token": email2, "user_id": str(self.user.id)},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        response_1 = self.client.post(
            reverse("PasswordResetTokenVerify"),
            {},
            format="json",
        )
        self.assertEqual(response_1.status_code, 400)

    def test_password_update(self):
        response = self.client.post(
            reverse("PasswordUpdate"),
            {
                "email": email1,
                "password": generate_random_password(),
                "confirm_password": generate_random_password(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 422)
        response_1 = self.client.post(
            reverse("PasswordUpdate"),
            {},
            format="json",
        )
        self.assertEqual(response_1.status_code, 422)

    def test_profile(self):
        response_1 = self.client.get(reverse("GetUserDetails"))
        self.assertEqual(response_1.status_code, 200)

    def test_change_password(self):
        response = self.client.patch(
            reverse("ChangePassword"),
            {},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(
            reverse("ChangePassword"),
            {
                "current_password": generate_random_password(),
                "new_password": generate_random_password(),
                "confirm_password": generate_random_password(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.patch(
            reverse("ChangePassword"),
            {
                "current_password": generate_random_password(),
                "new_password": "generate_random_password()",
                "confirm_password": "generate_random_password()",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
