from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("signup/", views.signup, name="signup"),
    path("posts/new/", views.post_create, name="post_create"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("posts/<int:pk>/comment/", views.comment_create, name="comment_create"),
    path("posts/<int:pk>/like-toggle/", views.like_toggle, name="like_toggle"),
    path("u/<str:username>/", views.profile_detail, name="profile_detail"),
    path("u/<str:username>/follow-toggle/", views.follow_toggle, name="follow_toggle"),
]