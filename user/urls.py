from django.urls import path
from user import views
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path("", views.UserView.as_view(), name="user_view"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh_pair"),
    path('api/ipark/token/', views.iParkTokenObtainPairView.as_view(), name='ipark_token'),
    path("kakao/", views.KakaoLoginView.as_view(), name="kakao"),
    path("myid/", views.FindUserInfoView.as_view(), name="myid_view"),
    path("alterpassword/", views.AlterPasswordView.as_view(), name="alter_password_view"),
    path("verification/", views.UserVerifyView.as_view(), name="user_verification_view"),
]
