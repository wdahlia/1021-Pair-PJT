from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"), # 메인 페이지
    path("movie/", views.movie, name="movie"), # 영화 등록
    path("movie/<int:movie_pk>", views.moviedetail, name="moviedetail"), # 영화 상세보기
    path("<int:movie_pk>/movie_delete/", views.movie_delete, name="movie_delete"), # 영화 삭제
    path("<int:movie_pk>/create", views.create, name="create"), # 리뷰 작성
    path("<int:review_pk>/", views.detail, name="detail"), # 리뷰 보기
    path("<int:review_pk>/update", views.update, name="update"), # 리뷰 수정
    path("<int:review_pk>/delete/", views.delete, name="delete"), # 리뷰 삭제
    path("<int:pk>/comments/", views.comment_create, name="comment_create"), # 댓글 작성
    path(
        "<int:review_pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ), # 댓글 삭제
]
