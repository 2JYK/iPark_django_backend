from django.urls import path
from user import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.UserView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]