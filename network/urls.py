
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like/<int:post_id>", views.like_toogle, name="like_toogle"),
    path("follow/<int:user_id>", views.follow_toogle, name="follow_toogle"),
    path("<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit")
]
