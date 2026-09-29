"""
تنظیمات پروژه‌ی آموزشی auth_tutorial

هدف: آموزش سیستم احراز هویت داخلی Django (django.contrib.auth)
"""
import os
from pathlib import Path

from django.contrib.messages import constants as message_constants

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# تنظیمات پایه (از متغیرهای محیطی خوانده می‌شود تا در production امن باشد)
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-insecure-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

# ---------------------------------------------------------------------------
# مرحله ۱: اپ‌های مربوط به احراز هویت
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    # سیستم احراز هویت: مدل User، Group، Permission، ویوها و فرم‌های آماده
    "django.contrib.auth",
    # auth برای ساختن Permission به ContentType نیاز دارد
    "django.contrib.contenttypes",
    # وضعیت لاگین بودن کاربر در session ذخیره می‌شود
    "django.contrib.sessions",
    # نمایش پیام‌های موفقیت/خطا
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # اپ خودمان (باید قبل از allauth بیاید تا قالب‌های سفارشی ما جایگزین قالب‌های allauth شوند)
    "accounts",
    # django-allauth: ثبت‌نام/ورود پیشرفته (ورود با ایمیل، تأیید ایمیل، بازیابی رمز، ...)
    "allauth",
    "allauth.account",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # محافظت در برابر CSRF (برای همین است که در فرم‌ها {% csrf_token %} می‌گذاریم)
    "django.middleware.csrf.CsrfViewMiddleware",
    # request.user را روی هر درخواست می‌گذارد
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # allauth: باید بعد از AuthenticationMiddleware و MessageMiddleware باشد
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "auth_tutorial.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                # متغیر {{ user }} را در همه‌ی قالب‌ها در دسترس می‌کند
                "django.contrib.auth.context_processors.auth",
                # متغیر {{ messages }} را در همه‌ی قالب‌ها در دسترس می‌کند
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "auth_tutorial.wsgi.application"

# ---------------------------------------------------------------------------
# دیتابیس: PostgreSQL (در داکر). برای اجرای سریع بدون داکر: DB_ENGINE=sqlite
# ---------------------------------------------------------------------------
if os.environ.get("DB_ENGINE") == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "bahram"),
            "USER": os.environ.get("POSTGRES_USER", "bahram"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "bahram123"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }

# ---------------------------------------------------------------------------
# اعتبارسنجی رمز عبور (هنگام ثبت‌نام اعمال می‌شود)
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# مراحل ۴ و ۸: آدرس‌های مربوط به ورود
# ---------------------------------------------------------------------------
# کاربر لاگین‌نشده که به صفحه‌ی محافظت‌شده برود، به این URL هدایت می‌شود
LOGIN_URL = "login"
# بعد از ورود موفق (اگر پارامتر next نباشد) به این صفحه می‌رود
LOGIN_REDIRECT_URL = "dashboard"
# توجه: LOGOUT_REDIRECT_URL را عمداً تنظیم نکرده‌ایم؛
# LogoutView صفحه‌ی logged_out.html را نمایش می‌دهد (مرحله ۶)

# ---------------------------------------------------------------------------
# django-allauth
# ---------------------------------------------------------------------------
# ModelBackend: ورود عادی Django (ادمین و LoginView خودمان)
# AuthenticationBackend: ورود allauth (مثلاً با ایمیل)
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# کاربر می‌تواند با نام کاربری «یا» ایمیل وارد شود
ACCOUNT_LOGIN_METHODS = {"username", "email"}
# فیلدهای ثبت‌نام (ستاره یعنی اجباری)
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
# optional: ایمیل تأیید فرستاده می‌شود ولی ورود منتظر تأیید نمی‌ماند
# mandatory: تا ایمیل تأیید نشود، ورود ممکن نیست
ACCOUNT_EMAIL_VERIFICATION = "optional"

# ایمیل‌ها در حالت آموزشی داخل لاگ کانتینر چاپ می‌شوند:
#   docker compose logs -f web
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "auth-tutorial@localhost"

# ---------------------------------------------------------------------------
# زبان و منطقه‌ی زمانی
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "fa"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# تبدیل سطح پیام Django به کلاس Bootstrap (error -> danger)
MESSAGE_TAGS = {
    message_constants.DEBUG: "secondary",
    message_constants.INFO: "info",
    message_constants.SUCCESS: "success",
    message_constants.WARNING: "warning",
    message_constants.ERROR: "danger",
}
