"""
فرم‌های ورود (مرحله ۳) و ثبت‌نام (مرحله ۷)
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class BootstrapFormMixin:
    """به همه‌ی فیلدها کلاس Bootstrap اضافه می‌کند."""

    def _apply_bootstrap(self):
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    """
    فرم ورود سفارشی؛ از AuthenticationForm ارث می‌برد.
    AuthenticationForm خودش authenticate() را صدا می‌زند و اگر نام کاربری
    یا رمز اشتباه باشد خطا می‌دهد؛ ما فقط ظاهر و متن‌ها را عوض می‌کنیم.
    """

    error_messages = {
        "invalid_login": "نام کاربری یا رمز عبور اشتباه است.",
        "inactive": "این حساب کاربری غیرفعال است.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        self.fields["username"].label = "نام کاربری"
        self.fields["password"].label = "رمز عبور"
        # نام کاربری و رمز را چپ‌چین (LTR) نمایش می‌دهیم چون انگلیسی وارد می‌شوند
        self.fields["username"].widget.attrs.update({"dir": "ltr", "autofocus": True})
        self.fields["password"].widget.attrs.update({"dir": "ltr"})


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    """
    فرم ثبت‌نام؛ از UserCreationForm ارث می‌برد و فیلد email را اضافه می‌کند.
    UserCreationForm خودش رمز را اعتبارسنجی و هش می‌کند (password1/password2).
    """

    email = forms.EmailField(label="ایمیل", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()
        self.fields["username"].label = "نام کاربری"
        self.fields["password1"].label = "رمز عبور"
        self.fields["password2"].label = "تکرار رمز عبور"
        for name in ("username", "email", "password1", "password2"):
            self.fields[name].widget.attrs["dir"] = "ltr"

    def clean_email(self):
        """اعتبارسنجی ایمیل تکراری (بدون توجه به بزرگی/کوچکی حروف)."""
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email


# test for class 