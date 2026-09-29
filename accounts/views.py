from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, SignUpForm

User = get_user_model()


# ---------------------------------------------------------------------------
# مرحله 1: تشخیص لاگین بودن کاربر ()
# ---------------------------------------------------------------------------
class HomeView(TemplateView):
    template_name = "accounts/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # در view از request.user.is_authenticated استفاده می‌کنیم
        context["view_says_authenticated"] = self.request.user.is_authenticated
        return context


# ---------------------------------------------------------------------------
# مرحله ۲: ورود با LoginView
# ---------------------------------------------------------------------------
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    # اگر کاربر از قبل وارد شده، فرم را نشانش نده و به LOGIN_REDIRECT_URL ببر
    redirect_authenticated_user = True

    def form_valid(self, form):
        # LoginView در form_valid همان login(request, user) را صدا می‌زند
        response = super().form_valid(form)
        messages.success(self.request, f"خوش آمدید {form.get_user().username}!")
        return response


# ---------------------------------------------------------------------------
# مرحله ۳: خروج با LogoutView
# ---------------------------------------------------------------------------
class CustomLogoutView(LogoutView):
    """
    از Django 5 به بعد LogoutView فقط درخواست POST را قبول می‌کند
    (برای جلوگیری از خروج اجباری با یک لینک ساده - حمله‌ی CSRF).
    چون next_page تنظیم نشده، قالب logged_out.html نمایش داده می‌شود.
    """

    template_name = "accounts/logged_out.html"


# ---------------------------------------------------------------------------
# مرحله ۴: ثبت‌نام با CreateView
# ---------------------------------------------------------------------------
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)  # کاربر ساخته و رمز هش می‌شود
        messages.success(self.request, "ثبت‌نام با موفقیت انجام شد. اکنون وارد شوید.")
        return response


# ---------------------------------------------------------------------------
# مرحله ۴ (مقصد ورود) و ۵: صفحات محافظت‌شده
# ---------------------------------------------------------------------------
class DashboardView(LoginRequiredMixin, TemplateView):
    """نسخه‌ی کلاسی محافظت: LoginRequiredMixin (معادل login_required)."""

    template_name = "accounts/dashboard.html"


@login_required  # نسخه‌ی تابعی محافظت؛ کاربر مهمان به LOGIN_URL?next=... می‌رود
def profile(request):
    return render(request, "accounts/profile.html")





# ---------------------------------------------------------------------------
# مرحله ۶: کوییز   test class DJ8
# ---------------------------------------------------------------------------
QUIZ_QUESTIONS = [
    {
        "id": "q1",
        "text": "تفاوت Authentication و Authorization چیست؟",
        "options": [
            "Authentication یعنی «چه کاری اجازه داری؟» و Authorization یعنی «تو کیستی؟»",
            "Authentication یعنی «تو کیستی؟» و Authorization یعنی «چه کاری اجازه داری؟»",
            "هر دو یک مفهوم هستند",
            "Authentication فقط برای ادمین است",
        ],
        "answer": 1,
        "explanation": "احراز هویت (Authentication) هویت را تأیید می‌کند؛ مجوزدهی (Authorization) سطح دسترسی را تعیین می‌کند.",
    },
    {
        "id": "q2",
        "text": "دکوریتور login_required چه کاری می‌کند؟",
        "options": [
            "کاربر را به‌طور خودکار لاگین می‌کند",
            "رمز عبور را هش می‌کند",
            "کاربر لاگین‌نشده را به LOGIN_URL هدایت می‌کند",
            "کاربر را از سایت خارج می‌کند",
        ],
        "answer": 2,
        "explanation": "اگر کاربر لاگین نباشد، به LOGIN_URL (همراه با پارامتر next) هدایت می‌شود.",
    },
    {
        "id": "q3",
        "text": "تفاوت LoginView و تابع authenticate() چیست؟",
        "options": [
            "authenticate() فقط اطلاعات را بررسی می‌کند و user یا None برمی‌گرداند؛ LoginView یک view کامل (فرم + بررسی + login + ریدایرکت) است",
            "LoginView فقط رمز را هش می‌کند",
            "هیچ تفاوتی ندارند",
            "authenticate() کاربر جدید می‌سازد",
        ],
        "answer": 0,
        "explanation": "authenticate() فقط اعتبار را بررسی می‌کند. ساخت session با login() انجام می‌شود که LoginView خودش صدایش می‌زند.",
    },
    {
        "id": "q4",
        "text": "خروج امن کاربر در Django 5 چگونه انجام می‌شود؟",
        "options": [
            "با یک لینک ساده (GET) به /accounts/logout/",
            "با فرم POST همراه با {% csrf_token %} به LogoutView",
            "با پاک کردن دستی کوکی‌ها در مرورگر",
            "با حذف کاربر از دیتابیس",
        ],
        "answer": 1,
        "explanation": "LogoutView فقط POST می‌پذیرد تا سایت‌های دیگر نتوانند کاربر را با یک لینک/تصویر از سایت شما خارج کنند.",
    },
    {
        "id": "q5",
        "text": "کدام گزینه درباره‌ی مدل User پیش‌فرض Django درست است؟",
        "options": [
            "رمز عبور به‌صورت متن ساده ذخیره می‌شود",
            "فیلدهایی مثل username، email، is_staff و is_active دارد",
            "فقط فیلد username دارد",
            "نمی‌توان با get_user_model() به آن دسترسی داشت",
        ],
        "answer": 1,
        "explanation": "رمز عبور به‌صورت هش ذخیره می‌شود و مدل User فیلدهایی مثل username، email، is_staff، is_active و is_superuser دارد.",
    },
]


class QuizView(View):
    template_name = "accounts/quiz.html"

    def get(self, request):
        return render(request, self.template_name, {"questions": QUIZ_QUESTIONS})

    def post(self, request):
        results = []
        score = 0
        for q in QUIZ_QUESTIONS:
            chosen = request.POST.get(q["id"])
            chosen_index = int(chosen) if chosen is not None and chosen.isdigit() else None
            correct = chosen_index == q["answer"]
            score += correct
            results.append(
                {
                    "text": q["text"],
                    "chosen": q["options"][chosen_index]
                    if chosen_index is not None and chosen_index < len(q["options"])
                    else None,
                    "correct_answer": q["options"][q["answer"]],
                    "is_correct": correct,
                    "explanation": q["explanation"],
                }
            )
        if score == len(QUIZ_QUESTIONS):
            messages.success(request, "آفرین! همه‌ی پاسخ‌ها درست بود.")
        else:
            messages.info(request, "پاسخ‌ها را مرور کنید و دوباره تلاش کنید.")
        context = {"results": results, "score": score, "total": len(QUIZ_QUESTIONS)}
        return render(request, "accounts/quiz_result.html", context)


# ---------------------------------------------------------------------------
# مرحله ۸: دموی تعاملی ماژول auth
# ---------------------------------------------------------------------------
class AuthDemoView(View):
    template_name = "accounts/auth_demo.html"

    def get(self, request):
        return render(request, self.template_name, self._base_context())

    def post(self, request):
        action = request.POST.get("action")
        context = self._base_context()

        if action == "authenticate":
            # authenticate() فقط بررسی می‌کند؛ session نمی‌سازد
            user = authenticate(
                request,
                username=request.POST.get("username", ""),
                password=request.POST.get("password", ""),
            )
            context["authenticate_result"] = (
                f"موفق: کاربر «{user.username}» پیدا شد (هنوز لاگین نشده!)"
                if user
                else "ناموفق: authenticate() مقدار None برگرداند."
            )

        elif action == "login":
            user = authenticate(
                request,
                username=request.POST.get("username", ""),
                password=request.POST.get("password", ""),
            )
            if user is not None:
                login(request, user)  # اینجا session ساخته می‌شود
                messages.success(request, f"login() برای «{user.username}» انجام شد.")
            else:
                messages.error(request, "authenticate() مقدار None داد؛ login() صدا زده نشد.")
            context = self._base_context()

        elif action == "logout":
            logout(request)  # session پاک می‌شود
            messages.info(request, "logout() صدا زده شد و session پاک شد.")
            context = self._base_context()

        elif action == "password":
            # کاربر موقت فقط در حافظه (ذخیره نمی‌شود) - تنها برای نمایش هش
            raw = request.POST.get("raw_password", "")
            check = request.POST.get("check_password", "")
            temp_user = User(username="demo")
            temp_user.set_password(raw)  # رمز را هش می‌کند
            context["hash_result"] = {
                "hash": temp_user.password,
                "check_input": check,
                "matches": temp_user.check_password(check),
            }

        return render(request, self.template_name, context)

    def _base_context(self):
        return {"user_model": f"{User.__module__}.{User.__name__}"}


# ---------------------------------------------------------------------------
# مرحله ۹: معرفی django-allauth (آدرس‌های خود allauth زیر /allauth/ هستند)
# ---------------------------------------------------------------------------
class AllauthInfoView(TemplateView):
    template_name = "accounts/allauth_info.html"
