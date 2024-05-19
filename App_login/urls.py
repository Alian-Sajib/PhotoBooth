from django.urls import path
from App_login import views

app_name = "App_login"

urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.login_page, name="login"),
    path("edit/", views.edit_profile, name="edit_profile"),
    path('profile/', views.profile, name="profile"),
    path('user/<username>/', views.user, name="user"),
    path('follow/<username>/', views.follow, name="follow"),
    path('unfollow/<username>/', views.unfollow, name="unfollow"),
]
