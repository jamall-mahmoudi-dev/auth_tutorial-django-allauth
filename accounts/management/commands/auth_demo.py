"""
دموی ماژول auth در خط فرمان:
    python manage.py auth_demo
"""
from django.contrib.auth import authenticate, get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "نمایش authenticate()، set_password()، check_password() و get_user_model()"

    def handle(self, *args, **options):
        # get_user_model() مدل User فعال پروژه را برمی‌گرداند
        User = get_user_model()
        self.stdout.write(f"مدل کاربر فعال: {User.__module__}.{User.__name__}")

        # پاک‌سازی اجرای قبلی (اگر نیمه‌کاره مانده باشد)
        User.objects.filter(username="cli_demo_user").delete()

        # create_user رمز را به‌صورت هش ذخیره می‌کند
        user = User.objects.create_user("cli_demo_user", "demo@example.com", "S3cret-Pass!")
        self.stdout.write(f"رمز ذخیره‌شده (هش): {user.password[:40]}...")

        # check_password رمز خام را با هش مقایسه می‌کند
        self.stdout.write(f"check_password (درست): {user.check_password('S3cret-Pass!')}")
        self.stdout.write(f"check_password (غلط):  {user.check_password('wrong')}")

        # set_password رمز را عوض و هش می‌کند (بعدش باید save() صدا زده شود)
        user.set_password("New-Pass-456!")
        user.save()
        self.stdout.write(f"بعد از set_password: {user.check_password('New-Pass-456!')}")

        # authenticate: user یا None برمی‌گرداند
        ok = authenticate(username="cli_demo_user", password="New-Pass-456!")
        bad = authenticate(username="cli_demo_user", password="S3cret-Pass!")
        self.stdout.write(f"authenticate (رمز جدید): {ok}")
        self.stdout.write(f"authenticate (رمز قدیمی): {bad}")

        # login() و logout() به request و session نیاز دارند؛ نمونه‌ی زنده‌شان در /auth-demo/ است
        user.delete()
        self.stdout.write(self.style.SUCCESS("کاربر آزمایشی حذف شد. پایان دمو."))
