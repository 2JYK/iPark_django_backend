from django.contrib import admin
from django.urls import path
from community import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('community/', views.CommunityView.as_view()),
]
