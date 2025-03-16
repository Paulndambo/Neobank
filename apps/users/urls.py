from django.urls import path

from apps.users.views import logout_user, register_user, verify_otp, login_user, otp_success

urlpatterns = [
    path("login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("verify-otp/", verify_otp, name="verify-otp"),
    path("otp-success/", otp_success, name="otp-success"),
    path("logout/", logout_user, name="logout"),
]
