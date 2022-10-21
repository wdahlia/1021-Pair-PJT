from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    reviews = Review.objects.order_by("-id")

    context = {
        "reviews": reviews,
    }

    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        create_form = ReviewForm(request.POST)
        if create_form.is_valid():
            review = create_form.save(commit=False)
            review.user = request.user
            create_form.save()
            return redirect("articles:index")

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
        update_form = ReviewForm(request.POST, instance=review)
        if update_form.is_valid():
            update_form.save()
            return redirect("articles:index")

    else:
        update_form = ReviewForm(instance=review)

    context = {
        "update_form": update_form,
    }

    return render(request, "articles/update.html", context)


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
