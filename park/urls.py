from django.urls import path
from park import views


urlpatterns = [
    path('<park_id>/', views.ParkView.as_view()),
    path('<park_id>/comment/', views.ParkCommentView.as_view()),
    path('<park_id>/comment/<comment_id>/', views.ParkCommentView.as_view())
]