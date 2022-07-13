from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("park/", include("park.urls")),
    path("user/", include("user.urls")),
    path("community/", include("community.urls")),
]

