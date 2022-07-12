from django.urls import path
from park import views


urlpatterns = [
    path('<park_id>/', views.ParkView.as_view())
]