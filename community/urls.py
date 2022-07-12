from django.urls import path
from community import views


urlpatterns = [
    path('', views.CommunityView.as_view()),
]
