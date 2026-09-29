# پروژه‌ی آموزشی احراز هویت در Django (  auth_tutorial  )

یک پروژه‌ی ساده و آموزشی برای یادگیری   سیستم احراز هویت داخلی Django   (  django.contrib.auth  )
با   Django 5.2  ،   PostgreSQL   و   Docker  . همه‌ی قالب‌ها فارسی و راست‌چین با Bootstrap 5 هستند.

## راه‌اندازی سریع (با Docker)

      
# ۱) (اختیاری) تنظیمات محیطی
cp .env.example .env

# ۲) ساخت و اجرای سرویس‌ها (پستگرس + Django). migrate خودکار اجرا می‌شود
docker compose up --build       # (بعد از اضافه شدن allauth حتماً --build بزنید)

# ۳) در ترمینال دیگر: ساخت ادمین
docker compose exec web python manage.py createsuperuser

# ۴) اجرای تست‌ها و دموی خط فرمان
docker compose exec web python manage.py test
docker compose exec web python manage.py auth_demo
      

سپس <http://localhost:8000> را باز کنید. پنل ادمین: <http://localhost:8000/admin/>

برای توقف:   docker compose down   (برای پاک کردن دیتابیس هم:   docker compose down -v  ).

> ایمیج‌های مورد استفاده:   python:3.11-slim-bullseye   و   postgres:17.11-trixie  
> (اگر قبلاً با   docker pull   گرفته باشید، دوباره دانلود نمی‌شوند).

## ساختار پروژه

      
auth_tutorial/
├── docker-compose.yml      # سرویس‌های db (postgres) و web (django)
├── Dockerfile
├── requirements.txt
├── manage.py
├── auth_tutorial/          # تنظیمات پروژه (settings.py, urls.py)
└── accounts/               # اپ آموزشی
    ├── forms.py            # LoginForm و SignUpForm
    ├── views.py            # همه‌ی ویوها (به ترتیب مراحل آموزشی)
    ├── urls.py
    ├── tests.py
    ├── management/commands/auth_demo.py
    └── templates/
        ├── accounts/       # base, home, login, signup, dashboard, profile, quiz, auth_demo, allauth_info, ...
        └── allauth/layouts/base.html   # اتصال صفحه‌های allauth به قالب فارسی/RTL ما
      

## مراحل آموزشی

### ۱. آشنایی با سیستم احراز هویت Django

Django دو اپ اصلی برای این کار دارد که در   INSTALLED_APPS   فعال شده‌اند:

-   django.contrib.auth  : مدل‌های User، Group و Permission، فرم‌ها و ویوهای آماده (LoginView و ...)
-   django.contrib.contenttypes  : auth برای ساخت Permissionها به آن نیاز دارد (هر Permission به یک مدل/ContentType وصل است)

سه مفهوم کلیدی:

-   User  : مدل کاربر با فیلدهایی مثل   username  ،   password   (هش‌شده)،   email  ،   is_active  ،   is_staff  ،   is_superuser  
-   Permission  : یک مجوز مشخص، مثل «اجازه‌ی حذف پست» (به‌طور خودکار برای هر مدل add/change/delete/view ساخته می‌شود)
-   Group  : مجموعه‌ای از Permissionها که می‌توان یک‌جا به چند کاربر داد

همچنین   SessionMiddleware   و   AuthenticationMiddleware   باعث می‌شوند در هر درخواست   request.user   در دسترس باشد.

### ۲. تشخیص لاگین بودن کاربر

- در قالب:   {% if user.is_authenticated %}   (فایل   home.html  )
- در view:   request.user.is_authenticated   (کلاس   HomeView  )
- کاربر مهمان (  AnonymousUser  ) همیشه   is_authenticated == False   دارد.

### ۳. فرم ورود (LoginForm)

  LoginForm   از   AuthenticationForm   ارث می‌برد؛ کلاس Bootstrap، برچسب‌های فارسی و پیام خطای فارسی اضافه شده است.

### ۴. احراز هویت با فرم (LoginView)

  CustomLoginView   با   form_class   و   template_name   تنظیم شده و در   settings.py  
مقدار   LOGIN_REDIRECT_URL = 'dashboard'   است؛ پس بعد از ورود موفق به داشبورد می‌رویم
(مگر اینکه پارامتر   next   وجود داشته باشد).

### ۵. کوییز

صفحه‌ی   /quiz/   پنج سؤال چندگزینه‌ای دارد. پاسخ‌ها در view بررسی و امتیاز نمایش داده می‌شود
(بدون ذخیره در دیتابیس).

### ۶. خروج (LogoutView)

- آدرس:   /accounts/logout/  
- از Django 5 به بعد   LogoutView     فقط POST   می‌پذیرد؛ به همین دلیل دکمه‌ی «خروج» یک فرم با   {% csrf_token %}   است
- دکمه‌ی خروج فقط برای کاربر لاگین‌شده نمایش داده می‌شود
- بعد از خروج قالب   logged_out.html   نمایش داده می‌شود

### ۷. ثبت‌نام (SignUpForm + CreateView)

  SignUpForm   از   UserCreationForm   ارث می‌برد و فیلد   email   و اعتبارسنجی ایمیل تکراری
(بدون حساسیت به بزرگی/کوچکی حروف) دارد. بعد از ثبت‌نام موفق، کاربر به صفحه‌ی ورود می‌رود.

  تفاوت   UserCreationForm   و فرم سفارشی:     UserCreationForm   فقط   username   و دو فیلد رمز را دارد
و رمز را اعتبارسنجی و هش می‌کند. با ارث‌بری از آن، همان منطق را نگه می‌داریم و فقط چیزهای
دلخواه (مثل email، اعتبارسنجی اضافه، ظاهر) را می‌افزاییم. فرم کاملاً سفارشی (  forms.Form  )
یعنی هش کردن رمز، اعتبارسنجی رمز و ساخت کاربر را خودتان باید بنویسید و احتمال خطای امنیتی بیشتر است.

### ۸. محافظت با login_required

-   profile  : تابعی با   @login_required   — آدرس   /accounts/profile/  
-   DashboardView  : کلاسی با   LoginRequiredMixin   — آدرس   /dashboard/  
-   LOGIN_URL = 'login'   تعیین می‌کند مهمان به کجا هدایت شود.

  پارامتر   next   چیست؟   وقتی مهمان به   /accounts/profile/   می‌رود، به
  /accounts/login/?next=/accounts/profile/   هدایت می‌شود. بعد از ورود موفق، Django کاربر را
به آدرس   next   برمی‌گرداند (و نه به   LOGIN_REDIRECT_URL  ). Django فقط آدرس‌های امن و هم‌دامنه را می‌پذیرد
تا از حمله‌ی Open Redirect جلوگیری شود.

### ۹. استفاده از ماژول auth

- صفحه‌ی تعاملی   /auth-demo/  :   authenticate()  ،   login()  ،   logout()  ،   set_password()  ،   check_password()  ،   get_user_model()  
- دموی خط فرمان:   python manage.py auth_demo  

### ۱۰. django-allauth

  django-allauth   یک پکیج خارجی است که روی   django.contrib.auth   سوار می‌شود و ورود، ثبت‌نام،
تأیید ایمیل، بازیابی رمز، مدیریت ایمیل‌ها و (در صورت فعال‌سازی) ورود با شبکه‌های اجتماعی را آماده می‌دهد.
در این پروژه   فقط   allauth.account     فعال است و آدرس‌هایش زیر   /allauth/   است تا با
پیاده‌سازی دستی مراحل ۳ تا ۸ مقایسه شود. توضیح و جدول مقایسه در صفحه‌ی   /allauth-info/   هم هست.

تغییرات لازم (همه در   settings.py   و   urls.py   انجام شده و کامنت دارند):

1.   django-allauth   در   requirements.txt  
2.   allauth   و   allauth.account   در   INSTALLED_APPS   (اپ   accounts   باید   قبل   از آن‌ها بیاید تا قالب‌های سفارشی ما جایگزین شوند)
3.   allauth.account.middleware.AccountMiddleware   در   MIDDLEWARE  
4.   AUTHENTICATION_BACKENDS   شامل   ModelBackend   و backend خود allauth
5.   path("allauth/", include("allauth.urls"))   در   urls.py  
6. تنظیمات   ACCOUNT_*   (ورود با نام کاربری یا ایمیل، فیلدهای ثبت‌نام، تأیید ایمیل)

نکات:

-   قالب فارسی/RTL:   فایل   accounts/templates/allauth/layouts/base.html   قالب پایه‌ی allauth را با قالب خودمان عوض می‌کند؛ پس همه‌ی صفحه‌های allauth (که ترجمه‌ی فارسی دارند) راست‌چین و با همان navbar نمایش داده می‌شوند.
-   ایمیل‌ها:   با   EMAIL_BACKEND   کنسولی، متن ایمیل تأیید و بازیابی رمز در لاگ چاپ می‌شود:   docker compose logs -f web  
-   تأیید ایمیل:   مقدار   ACCOUNT_EMAIL_VERIFICATION = "optional"   است؛ با   "mandatory"   تا تأیید ایمیل ورود ممکن نیست.
-   خروج:     /allauth/logout/   یک صفحه‌ی تأیید نشان می‌دهد و با POST خارج می‌کند (مثل مرحله‌ی ۶).
-   ورود با گوگل/گیت‌هاب:   با افزودن   allauth.socialaccount   و   allauth.socialaccount.providers.google   به   INSTALLED_APPS   و ساختن کلید OAuth در کنسول ارائه‌دهنده. این بخش عمداً فعال نشده چون به کلید و حساب توسعه‌دهنده نیاز دارد.

## لیست URLها

   آدرس    کاربرد   
  ---  ---  
     /      خانه؛ نمایش وضعیت لاگین (مرحله ۲)   
     /dashboard/      داشبورد محافظت‌شده با   LoginRequiredMixin     
     /accounts/login/      فرم ورود (  LoginView  )   
     /accounts/logout/      خروج (فقط POST)   
     /accounts/signup/      ثبت‌نام (  CreateView  )   
     /accounts/profile/      پروفایل با   @login_required     
     /quiz/      کوییز آموزشی   
     /auth-demo/      دموی تعاملی ماژول auth   
     /allauth-info/      معرفی allauth و مقایسه با پیاده‌سازی دستی   
     /allauth/signup/      ثبت‌نام با allauth   
     /allauth/login/      ورود با allauth (نام کاربری یا ایمیل)   
     /allauth/logout/      خروج با allauth   
     /allauth/password/reset/      بازیابی رمز عبور   
     /allauth/password/change/      تغییر رمز (نیاز به ورود)   
     /allauth/email/      مدیریت ایمیل‌ها (نیاز به ورود)   
     /admin/      پنل مدیریت   

## نکات امنیتی مهم

-   CSRF:   همه‌ی فرم‌های POST باید   {% csrf_token %}   داشته باشند. بدون آن Django درخواست را رد می‌کند (خطای 403).
-   Password hashing:   Django رمز را هرگز به‌صورت متن ساده ذخیره نمی‌کند؛ به‌طور پیش‌فرض با PBKDF2-SHA256 و salt هش می‌شود. هرگز فیلد   password   را مستقیم مقداردهی نکنید؛ از   set_password()   یا   create_user()   استفاده کنید.
-   HTTPS در production:   بدون HTTPS نام کاربری و رمز در شبکه قابل شنود است. در production این‌ها را فعال کنید:   SECURE_SSL_REDIRECT = True  ،   SESSION_COOKIE_SECURE = True  ،   CSRF_COOKIE_SECURE = True   و   SECURE_HSTS_SECONDS  .
-   کلید و debug:     DJANGO_SECRET_KEY   را در production تغییر دهید و   DJANGO_DEBUG=0   بگذارید. مقدارهای پیش‌فرض این پروژه فقط برای آموزش‌اند.
-   allauth:   در production مقدار   ACCOUNT_EMAIL_VERIFICATION = "mandatory"   و یک   EMAIL_BACKEND   واقعی (SMTP) بگذارید؛ backend کنسولی فقط برای آموزش است.
-   رمز دیتابیس:   مقادیر پیش‌فرض   POSTGRES_PASSWORD   فقط برای توسعه‌ی محلی‌اند؛ در   .env   عوض کنید.
-   اعتبارسنجی رمز:     AUTH_PASSWORD_VALIDATORS   در ثبت‌نام اعمال می‌شود (حداقل طول، رمز رایج، فقط عدد، شباهت به نام کاربری).
-   پیام خطای ورود مبهم:   پیام «نام کاربری یا رمز عبور اشتباه است» عمداً مشخص نمی‌کند کدام‌یک غلط بوده.
-   خروج با POST:   برای جلوگیری از خروج اجباری کاربر با یک لینک یا تصویر در سایت دیگر.

## جدول مقایسه‌ی توابع و کلاس‌های auth

   نام    نوع    کار می‌کند    نکته   
  ---  ---  ---  ---  
     authenticate()      تابع    نام کاربری/رمز را بررسی و   User   یا   None   برمی‌گرداند    session نمی‌سازد   
     login(request, user)      تابع    کاربر را در session ثبت می‌کند    بعد از   authenticate()   صدا زده می‌شود   
     logout(request)      تابع    session را پاک می‌کند    داده‌های session هم پاک می‌شود   
     get_user_model()      تابع    مدل User فعال پروژه را برمی‌گرداند    بهتر از import مستقیم   User     
     user.set_password()      متد    رمز را هش می‌کند    بعدش   save()   لازم است   
     user.check_password()      متد    رمز خام را با هش مقایسه می‌کند      True/False     
     LoginView      کلاس    فرم + authenticate + login + ریدایرکت      form_class  ,   template_name     
     LogoutView      کلاس    logout و نمایش قالب/ریدایرکت    فقط POST (از Django 5)   
     AuthenticationForm      فرم    فرم ورود آماده    خودش   authenticate()   را صدا می‌زند   
     UserCreationForm      فرم    فرم ثبت‌نام آماده    رمز را اعتبارسنجی و هش می‌کند   
     @login_required      دکوریتور    محافظت از view تابعی    ریدایرکت به   LOGIN_URL?next=...     
     LoginRequiredMixin      mixin    محافظت از view کلاسی    معادل   login_required     
     allauth.account      اپ خارجی    ورود/ثبت‌نام/تأیید ایمیل/بازیابی رمز آماده    زیر   /allauth/     

## اجرای بدون Docker (اختیاری)

 برای آزمایش سریع بدون پستگرس دیتا بیس:

      bash
pip install -r requirements.txt
export DB_ENGINE=sqlite
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
      
