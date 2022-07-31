from django.urls import path
from community import views


urlpatterns = [
    path("", views.CommunityView.as_view(), name="community_view"),
    path("search/", views.CommunitySearchView.as_view()),
    path("<int:article_id>/", views.CommunityDetailView.as_view()),
    path("<int:article_id>/comment/", views.CommentView.as_view()),
    path("comment/<int:comment_id>/", views.CommentView.as_view()),
]
