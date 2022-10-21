from django.shortcuts import render, redirect
from .models import Review, Comment, Movie
from .forms import ReviewForm, CommentForm, MovieForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min, Sum

# Create your views here.


def index(request):
    reviews = Review.objects.all()
    movies = Movie.objects.all()
    context = {
        "reviews": reviews,
        "movies": movies,
    }

    return render(request, "articles/index.html", context)


@login_required
def create(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.method == "POST":
        create_form = ReviewForm(request.POST)
        if create_form.is_valid():
            review = create_form.save(commit=False)
            review.user = request.user
            review.movie = movie
            create_form.save()
            return redirect("articles:moviedetail", movie_pk)

    else:
        create_form = ReviewForm()

    context = {
        "create_form": create_form,
    }

    return render(request, "articles/create.html", context)


@login_required
def delete(request, review_pk):
    Review.objects.get(pk=review_pk).delete()
    return redirect("articles:index")


@login_required
def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm()
    comments = review.comment_set.all()
    context = {
        "review": review,
        "comment_form": comment_form,
        "comments": comments,
    }

    return render(request, "articles/detail.html", context)


@login_required
def update(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == "POST":
        create_form = ReviewForm(request.POST, instance=review)
        if create_form.is_valid():
            create_form.save()
            return redirect("articles:detail", review_pk)
    else:
        create_form = ReviewForm(instance=review)

    context = {
        "create_form": create_form,
    }

    return render(request, "articles/create.html", context)


@login_required
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect("articles:detail", pk)


@login_required
def comment_delete(request, review_pk, comment_pk):
    Comment.objects.get(pk=comment_pk).delete()
    return redirect("articles:detail", review_pk)


@login_required
def movie(request):
    if request.method == "POST":
        movie_form = MovieForm(request.POST, request.FILES)
        if movie_form.is_valid():

            movie_form.save()
            return redirect("articles:index")
    else:
        movie_form = MovieForm()

    context = {
        "movie_form": movie_form,
    }

    return render(request, "articles/movie.html", context)


@login_required
def moviedetail(request, movie_pk):
    reviews = Review.objects.filter(movie=movie_pk)
    movie = Movie.objects.get(pk=movie_pk)
    grade = reviews.aggregate(avg=Avg("grade"))
    cnt = reviews.count()
    avg = "리뷰 없음"
    star = ""
    if grade["avg"]:
        if grade["avg"] > 9.8:
            star = "★★★★★"
        elif grade["avg"] > 8.8:
            star = "★★★★☆"
        elif grade["avg"] > 7.8:
            star = "★★★★"
        elif grade["avg"] > 6.8:
            star = "★★★☆"
        elif grade["avg"] > 5.8:
            star = "★★★"
        elif grade["avg"] > 4.8:
            star = "★★☆"
        elif grade["avg"] > 3.8:
            star = "★★"
        elif grade["avg"] > 2.8:
            star = "★☆"
        elif grade["avg"] > 1.8:
            star = "★"
        elif grade["avg"] > 0.8:
            star = "☆"
        else:
            avg = ""
        avg = round(grade["avg"] / 2, 1)
    context = {
        "movie": movie,
        "reviews": reviews,
        "star": star,
        "avg": avg,
        "cnt": cnt,
    }
    return render(request, "articles/moviedetail.html", context)


@login_required
def movie_delete(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    movie.delete()
    return redirect("articles:index")
