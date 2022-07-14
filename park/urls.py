from django.urls import path
from park import views


urlpatterns = [
    path("search/", views.ParkSearchView.as_view(), name="park_search"),
    path("<park_id>/", views.ParkView.as_view(), name="park"),
    path("<park_id>/comment/", views.ParkCommentView.as_view(), name="park_comment_create"), 
    path("<park_id>/comment/<comment_id>/", views.ParkCommentView.as_view(), name="park_comment_manage"),
]