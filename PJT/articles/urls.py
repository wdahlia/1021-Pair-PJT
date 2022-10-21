from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:movie_pk>/create", views.create, name="create"),
    path("movie/", views.movie, name="movie"),
    path("movie/<int:movie_pk>", views.moviedetail, name="moviedetail"),
    path("<int:review_pk>/", views.detail, name="detail"),
    path("<int:review_pk>/update", views.update, name="update"),
    path("<int:review_pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
    path(
        "<int:review_pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path("<int:movie_pk>/movie_delete/", views.movie_delete, name="movie_delete"),
]
