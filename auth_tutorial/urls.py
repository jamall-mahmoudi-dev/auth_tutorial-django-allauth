from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # آدرس‌های django-allauth زیر /allauth/ (جدا از پیاده‌سازی دستی ما)
    path("allauth/", include("allauth.urls")),
    # همه‌ی آدرس‌های اپ accounts (خانه، ورود، خروج، ثبت‌نام، ...)
    path("", include("accounts.urls")),
]
