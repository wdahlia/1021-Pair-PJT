from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<int:pk>", views.profile, name="profile"),
    path("userlist/", views.userlist, name="userlist"),
    path("update/", views.update, name="update"),
    path("password/", views.change_password, name="change_password"),
    path("delete/", views.delete, name="delete"),
]
