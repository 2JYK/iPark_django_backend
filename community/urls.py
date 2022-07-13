from django.urls import path
from community import views


urlpatterns = [
    path("", views.CommunityView.as_view(), name="community_view"),
    path("comment/", views.CommentView.as_view()),
    path("comment/<comment_id>", views.CommentView.as_view()),
]