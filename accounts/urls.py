from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("accounts/login/", views.CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/profile/", views.profile, name="profile"),
    path("quiz/", views.QuizView.as_view(), name="quiz"),
    path("auth-demo/", views.AuthDemoView.as_view(), name="auth_demo"),
    path("allauth-info/", views.AllauthInfoView.as_view(), name="allauth_info"),
]
