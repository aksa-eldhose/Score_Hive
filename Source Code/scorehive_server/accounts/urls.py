from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (ChangePassword, CheckCurrentPassword, EditProfile,
                    EmailVerify, Login, PasswordUpdate, RegisterUser,
                    ResetTokenVerification, UserAccountPasswordReset,
                    UserRegister)

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="test"),
    path("registerTokenVerify/", EmailVerify.as_view(), name="emailTokenVerification"),
    path("registerUserDetails/", UserRegister.as_view(), name="userDetailsSubmission"),
    path("login/", Login.as_view(), name="userLogin"),
    path("accessTokenRefresh/", TokenRefreshView.as_view(), name="refreshAccessToken"),
    path("forgotPassword/", UserAccountPasswordReset.as_view(), name="passwordReset"),
    path(
        "resetPasswordToken/",
        ResetTokenVerification.as_view(),
        name="PasswordResetTokenVerify",
    ),
    path("resetPassword/", PasswordUpdate.as_view(), name="PasswordUpdate"),
    path("getUserDetails/", EditProfile.as_view(), name="GetUserDetails"),
    path("changePassword/", ChangePassword.as_view(), name="ChangePassword"),
    path(
        "checkCurrentPassword/",
        CheckCurrentPassword.as_view(),
        name="checkCurrentPassword",
    ),
]
