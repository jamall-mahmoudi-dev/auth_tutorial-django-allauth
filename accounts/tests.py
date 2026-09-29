from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class HomeTests(TestCase):
    def test_guest_sees_guest_message(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "شما مهمان هستید")
        self.assertNotContains(response, "خروج")  # دکمه‌ی خروج فقط برای لاگین‌شده‌ها

    def test_logged_in_user_sees_username_and_logout_button(self):
        User.objects.create_user("ali", password="Str0ng-pass!")
        self.client.login(username="ali", password="Str0ng-pass!")
        response = self.client.get(reverse("home"))
        self.assertContains(response, "ali")
        self.assertContains(response, "خروج")
        self.assertTrue(response.context["view_says_authenticated"])


class LoginTests(TestCase):
    def setUp(self):
        User.objects.create_user("ali", "ali@example.com", "Str0ng-pass!")

    def test_login_redirects_to_dashboard(self):
        response = self.client.post(
            reverse("login"), {"username": "ali", "password": "Str0ng-pass!"}
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_wrong_password_shows_error(self):
        response = self.client.post(reverse("login"), {"username": "ali", "password": "bad"})
        self.assertContains(response, "نام کاربری یا رمز عبور اشتباه است.")

    def test_next_parameter_is_respected(self):
        response = self.client.post(
            reverse("login") + "?next=/accounts/profile/",
            {"username": "ali", "password": "Str0ng-pass!", "next": "/accounts/profile/"},
        )
        self.assertRedirects(response, reverse("profile"))


class ProtectedViewTests(TestCase):
    def test_profile_redirects_guest_to_login_with_next(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('profile')}")

    def test_dashboard_redirects_guest(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_profile_ok_for_user(self):
        User.objects.create_user("ali", password="Str0ng-pass!")
        self.client.login(username="ali", password="Str0ng-pass!")
        self.assertEqual(self.client.get(reverse("profile")).status_code, 200)


class LogoutTests(TestCase):
    def setUp(self):
        User.objects.create_user("ali", password="Str0ng-pass!")
        self.client.login(username="ali", password="Str0ng-pass!")

    def test_logout_requires_post(self):
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)

    def test_logout_post_ends_session_and_shows_template(self):
        response = self.client.post(reverse("logout"))
        self.assertTemplateUsed(response, "accounts/logged_out.html")
        self.assertEqual(self.client.get(reverse("profile")).status_code, 302)


class SignUpTests(TestCase):
    data = {
        "username": "sara",
        "email": "sara@example.com",
        "password1": "Str0ng-pass!",
        "password2": "Str0ng-pass!",
    }

    def test_signup_creates_user_and_redirects_to_login(self):
        response = self.client.post(reverse("signup"), self.data)
        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="sara")
        self.assertNotEqual(user.password, "Str0ng-pass!")  # هش شده است
        self.assertTrue(user.check_password("Str0ng-pass!"))

    def test_duplicate_email_rejected_case_insensitive(self):
        User.objects.create_user("old", "SARA@example.com", "Str0ng-pass!")
        response = self.client.post(reverse("signup"), self.data)
        self.assertContains(response, "این ایمیل قبلاً ثبت شده است.")
        self.assertFalse(User.objects.filter(username="sara").exists())


class QuizTests(TestCase):
    def test_perfect_score(self):
        answers = {"q1": 1, "q2": 2, "q3": 0, "q4": 1, "q5": 1}
        response = self.client.post(reverse("quiz"), answers)
        self.assertEqual(response.context["score"], 5)

    def test_empty_submission_scores_zero(self):
        response = self.client.post(reverse("quiz"), {})
        self.assertEqual(response.context["score"], 0)


class AuthDemoTests(TestCase):
    def setUp(self):
        User.objects.create_user("ali", password="Str0ng-pass!")

    def test_authenticate_does_not_login(self):
        response = self.client.post(
            reverse("auth_demo"),
            {"action": "authenticate", "username": "ali", "password": "Str0ng-pass!"},
        )
        self.assertContains(response, "هنوز لاگین نشده")
        self.assertFalse(response.context["user"].is_authenticated)

    def test_login_action_logs_in(self):
        response = self.client.post(
            reverse("auth_demo"),
            {"action": "login", "username": "ali", "password": "Str0ng-pass!"},
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_password_hash_demo(self):
        response = self.client.post(
            reverse("auth_demo"),
            {"action": "password", "raw_password": "abc12345", "check_password": "abc12345"},
        )
        self.assertTrue(response.context["hash_result"]["matches"])
        self.assertTrue(response.context["hash_result"]["hash"].startswith("pbkdf2_sha256$"))


class AllauthTests(TestCase):
    """تست‌های django-allauth (آدرس‌ها زیر /allauth/ هستند)."""

    def test_pages_render_with_our_rtl_layout(self):
        for name in ("account_login", "account_signup", "account_reset_password"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)
            self.assertContains(response, 'dir="rtl"')
            self.assertContains(response, "allauth-page")

    def test_info_page(self):
        self.assertEqual(self.client.get(reverse("allauth_info")).status_code, 200)

    def test_signup_creates_user_and_sends_confirmation_email(self):
        from django.core import mail

        response = self.client.post(
            reverse("account_signup"),
            {
                "email": "neda@example.com",
                "username": "neda",
                "password1": "Str0ng-pass!",
                "password2": "Str0ng-pass!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="neda").exists())
        self.assertEqual(len(mail.outbox), 1)  # ایمیل تأیید (verification=optional)

    def test_login_with_email_or_username(self):
        User.objects.create_user("ali", "ali@example.com", "Str0ng-pass!")
        for login in ("ali@example.com", "ali"):
            self.client.logout()
            response = self.client.post(
                reverse("account_login"), {"login": login, "password": "Str0ng-pass!"}
            )
            self.assertRedirects(response, reverse("dashboard"), msg_prefix=login)

    def test_manual_pages_still_work_alongside_allauth(self):
        User.objects.create_user("ali", "ali@example.com", "Str0ng-pass!")
        response = self.client.post(reverse("login"), {"username": "ali", "password": "Str0ng-pass!"})
        self.assertRedirects(response, reverse("dashboard"))
