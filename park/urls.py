from django.urls import path
from park import views


urlpatterns = [
    path("", views.ToggleParkView.as_view(), name="toggle_park"),
    path("option/", views.OptionView.as_view(), name="park_search"),
    path("popularity/", views.ParkPopularityView.as_view(), name="park_popularity"),
    path("<park_id>/", views.ParkView.as_view(), name="park"),
    path("<park_id>/comment/", views.ParkCommentView.as_view(), name="park_comment_create"), 
    path("comment/<comment_id>/", views.ParkCommentView.as_view(), name="park_comment_manage"),
]