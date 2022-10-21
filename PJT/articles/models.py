from email.policy import default
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from multiselectfield import MultiSelectField


# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=30)
    summary = models.TextField()
    director = models.CharField(max_length=20)
    runningtime = models.IntegerField(default=50)
    releasedate = models.DateField(null=True)
    genrelist = (
        ("SF", "SF"),
        ("드라마", "드라마"),
        ("액션", "액션"),
        ("모험", "모험"),
        ("판타지", "판타지"),
        ("멜로", "멜로"),
        ("코미디", "코미디"),
        ("느와르", "느와르"),
        ("히어로", "히어로"),
        ("공포", "공포"),
        ("하이틴", "하이틴"),
    )
    jenre = MultiSelectField(
        choices=genrelist,
        min_choices=1,
        max_choices=3,
    )
    image = ProcessedImageField(
        blank=True,
        upload_to="images/",
        processors=[ResizeToFill(720, 480)],
        format="JPEG",
        options={"quality": 100},
    )
    thumbnail = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(700, 1000)],
        format="JPEG",
        options={"quality": 80},
    )


class Review(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    grade = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
