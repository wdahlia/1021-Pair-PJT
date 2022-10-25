# 221021 Pair Project

> **영화 정보, 리뷰 사이트 구현**
>
> 김광표, 임선주, 류진숙

<br>

`🔒 실습 목차`

- [네비게이션 바](#네비게이션-바)


- [Accounts App](#accounts-app)
  - [회원 가입](#회원-가입)
  - [로그인](#로그인)
  - [로그아웃](#로그아웃)
  - [Userlist 페이지](#userlist-페이지)
  - [Profile 페이지](#profile-페이지)
  - [Profile Update 페이지](#profile-update-페이지)
  - [Change Password 페이지](#change-password-페이지)
- [Articles App](#articles-app)
  - [Movie create 페이지](#movie-create-페이지)
  - [Index 페이지](#index-페이지)
  - [Moive detail 페이지](#moive-detail-페이지)
  - [Review create 페이지](#review-create-페이지)
  - [Review Update 페이지](#review-update-페이지)
  - [comments](#comments)

<br>


### 네비게이션 바

* 공통

  * 홈버튼, 유저리스트 버튼(login required)
  * 영화 검색창
    * 영화들을 검색 가능하며, 아무것도 입력하지 않거나 리스트에 없는 영화를 검색한 경우 No result가 출력되며, 리스트에 있는 영화를 검색한 경우 해당 영화의 포스터가 출력된다.

* 로그인시

  * 로그아웃 버튼, 회원 프로필 버튼

    <p align="center"><img src="https://user-images.githubusercontent.com/108653518/197585005-9b7f822e-5506-406e-ab60-7e15be20c21c.png" alt="login"  /></p>

    

* 비 로그인시

  * 로그인 버튼, 회원가입 버튼

    <p align="center"><img src="https://user-images.githubusercontent.com/108653518/197585028-b5d39ad3-f5d3-4e92-afcf-fcc3b93a9871.png" alt="logout"  /></p>

<br>

## Accounts App

### 회원 가입

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197585344-2e49615a-67b9-4a1f-a2d4-a38bf403ff87.png" alt="signup"  /></p>

- Django **AbstractUser 모델** 상속

  ```python
  from django.contrib.auth.models import AbstractUser
  
  
  class User(AbstractUser):
      pass
  ```

- Django **내장폼 UserCreationForm**을 상속받은 `CustomUserCreationForm` 사용

  ```python
  from django.contrib.auth import get_user_model
  from django.contrib.auth.forms import UserCreationForm
  
  class CustomUserCreationForm(UserCreationForm):
      class Meta(UserCreationForm.Meta):
          model = get_user_model()
          fields = (
              "username",
              "email",
              "first_name",
              "last_name",
          )
  ```

  - 아이디, 이메일, 성과 이름을 입력

```python
# urls.py
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
  path("signup/", views.signup, name="signup"),
]
```

```python
# views.py
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            form.save()
            auth_login(request, user)
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/signup.html", context)
```

---

<br>

### 로그인

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197585020-8311daed-a20f-418c-84ea-ce8b149267e1.png" alt="login1"  /></p>

- 내장 폼 AuthenticationForm 활용
- 로그인시 message alert

```python
# urls.py
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
  path("login/", views.login, name="login"),
]
```

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, "로그인 되었습니다.")
            return redirect("articles:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)
```

```html
<!-- login.html -->
{% extends 'base.html' %}
{% block content %}
  {% load django_bootstrap5 %}
  <div class="container d-flex justify-content-center py-5">
    <div class="card col-6 review-detail">
        {% comment %} <div class="review-detail rounded-4 shadow-lg p-5"> {% endcomment %}
      <h1 class="text-center mt-5 fs-3 fw-bold text-white">Login</h1>
      <div class="card-body">
        <form action="{% url 'accounts:login' %}" method="POST" class="text-dark px-5 py-3">
          {% csrf_token %}
          {% bootstrap_form form %}
          <div class="d-grid gap-2">
            <button class="btn btn-warning mt-5 mb-2" type="submit">Login</button>
            <a class="btn btn-outline-warning text-black" href="{% url 'accounts:signup' %}" role="button">Create Account</a>
          </div>
        </form>
      </div>
    </div>
  </div>
{% endblock content %}
```

```html
<!-- base.html -->
<!-- guest (navbar) -->
{% else %}
<ul class="navbar-nav">
  <li class="nav-item mx-2">
    <a class="nav-link" href="{% url 'accounts:login' %}">Hello, Guest</a>
  </li>
  <a class="nav-link" href="{% url 'accounts:login' %}">Login</a>
  <a class="nav-link" href="{% url 'accounts:signup' %}">SingUp</a>
</ul>
{% endif %}
```

---

<br>

### 로그아웃

- 로그아웃시 message alert

```python
# urls.py
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
  path("logout/", views.logout, name="logout"),
]
```

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "로그아웃 되었습니다.")
    return redirect("articles:index")
```

```html
<!-- base.html -->  
<!-- 로그인한 경우 (navbar) -->
{% if user.is_authenticated %}
<ul class="navbar-nav">
  <li class="nav-item mx-2">
    <a class="nav-link" href="{% url 'accounts:profile' user.pk %}">Hello,
      {{ request.user.username }}</a>
  </li>
  <a class="nav-link mx-2" href="{% url 'accounts:logout' %}">Logout</a>
</ul>
```

---

<br>

### Userlist 페이지 

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197585682-3255f1cb-6c59-411c-aaa3-a87a7ba66e97.png" alt="userlist"  /></p>

- random 라이브러리를 import해서 사진들의 이미지 주소를 담은 profile 리스트에서 사진 하나씩을 랜덤으로 지정해주었다.
  - 새로고침 시 이미지 랜덤으로 변화
- 유저 이미지, 이메일, 유저 아이디, 가입 일 표시

```python
# urls.py
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
  path("userlist/", views.userlist, name="userlist"),
]
```

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import User
from django.contrib import messages
import random

@login_required
def userlist(request):
    users = User.objects.all()
    profile = ['https://cdn.pixabay.com/photo/2021/04/05/15/55/neptune-6153867_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/48/earth-6153854_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/52/jupiter-6153859_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/44/venus-6153849_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/53/saturn-6153860_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/44/mercury-6153848_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/48/moon-6153855_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/52/mars-6153858_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/54/uranus-6153865_960_720.png']

    profile_image = random.choice(profile)
 
    context = {
        "profile_image": profile_image,
        "users": users,
    }
    return render(request, "accounts/userlist.html", context)
```

```html
<!-- userlist.html -->
{% extends 'base.html' %}
{% load static %}
{% load django_bootstrap5 %}
{% block content %}
  <div class="container py-5">
    <div class="text-center text-white">
      <h2>User List</h2>
    </div>
    <div class="row row-cols-1 row-cols-md-2">
      {% for user in users %}
        <div class="col g-4 text-center">
          <div class="card h-100 m-4 text-white">
            <div class="card-body">
              <img src="{{ profile_image }}" style="width: 10rem; height:10rem;" class="shadow-lg mb-3">
              <h4 class="card-subtitle my-2">{{ user.last_name }}{{ user.first_name }}</h4>
              <hr>
              <div class="p-3 text-white text-bg-white opacity-75">
                <h4 class="card-subtitle my-2 text-warning">
                  {{ user.email }}</h4>
                <p class="card-text m-0">user no.
                  {{ user.pk }}</p>
                <p class="card-text fs-6">joined at
                  {{ user.date_joined|date:'Y-m-d H:i:s' }}</p>
              </div>
            </div>
          </div>
        </div>
      {% endfor %}
    </div>
  </div>
{% endblock content %}
```

<hr>


<br>

### Profile 페이지

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197585827-813cfc52-b1e1-4943-95d2-0c477a822dd0.png" alt="profile"  /></p>

- random 라이브러리를 import해서 사진들의 이미지 주소를 담은 profile 리스트에서 사진 하나씩을 랜덤으로 지정해주었다.
  - 새로고침 시 이미지 랜덤으로 변화
- 로그인한 user의 pk값을 받아와서 데이터베이스안의 일치하는 pk를 user라는 변수에 저장하여 그 값을 html에 받아온다

```python
# urls.py
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
  path("<int:pk>", views.profile, name="profile"),
]
```

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.decorators import login_required
import random


@login_required
def profile(request, pk):
    user = User.objects.get(pk=pk)
    profile = ['https://cdn.pixabay.com/photo/2021/04/05/15/55/neptune-6153867_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/48/earth-6153854_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/52/jupiter-6153859_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/44/venus-6153849_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/53/saturn-6153860_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/44/mercury-6153848_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/48/moon-6153855_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/52/mars-6153858_960_720.png',
    'https://cdn.pixabay.com/photo/2021/04/05/15/54/uranus-6153865_960_720.png']

    profile_image = random.choice(profile)
    context = {
        "profile_image": profile_image,
        "user": user,
    }
    return render(request, "accounts/profile.html", context)
```

```html
<!-- profile.html -->
{% extends 'base.html' %}
{% block content %}
  {% load django_bootstrap5 %}

  <div class="container d-flex flex-column align-items-center py-5">
    <div class="card mt-5 mb-4 border border-light" style="width: 25rem;">
      <div class="card-header border border-light text-white opacity-75">
        <h5 class="fs-3 fw-bold text-center my-1">
          {{ user.username }}
        </h5>
      </div>
      <div class="card-body d-flex justify-content-center">
        <img src="{{ profile_image }}" class="card-img-top rounded-1" style="width: 20rem; height: 20rem;" alt="...">
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <i class="bi bi-hash me-2"></i>
          User No.
          {{ user.pk }}</li>
        <li class="list-group-item">
          <i class="bi bi-person-fill me-2"></i>
          {{ user.first_name }}
          {{ user.last_name }}</li>
        <li class="list-group-item">
          <i class="bi bi-envelope-fill me-2"></i>
          {{ user.email }}</li>
        <li class="list-group-item">
          <i class="bi bi-calendar-check-fill me-2"></i>
          joined at
          {{ user.date_joined|date:'Y-m-d H:i' }}</li>
      </ul>
    </div>
	</div>
{% endblock content %}
```

<hr>


<br>

### Profile Update 페이지

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197585919-0c24ccec-48c9-47c5-bb9c-b89646929d03.jpeg" alt="profileupdate"  /></p>

- Profile에서 `Edit My Info`를 클릭하면 이메일 주소, 이름, 성을 수정할 수 있는 폼을 출력해준다

```python
# urls.py
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
  path("update/", views.update, name="update"),
]
```

```python
# views.py
from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required

@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "회원정보 수정이 완료되었습니다.")
            return redirect("articles:index")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)
```

```html
<!-- profile.html -->
{% if request.user == user %}
  <div class="mb-5 d-flex justify-content-end">
    <div class="btn-group" role="group">
      <button type="button" class="btn btn-warning dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
        Edit
      </button>
      <ul class="dropdown-menu">
        <li>
          <a class="dropdown-item" href="{% url 'accounts:update' %}" role="button">Edit My Info</a>
        </li>
        <li>
          <hr class="dropdown-divider">
        </li>
        <li>
          <a class="dropdown-item" href="{% url 'accounts:change_password' %}" role="button">Change Password</a>
        </li>
        <li>
          <hr class="dropdown-divider">
        </li>
        <li>
          <a class="dropdown-item text-danger" href="{% url 'accounts:delete' %}" role="button">Delete Account</a>
        </li>
      </ul>
    </div>
    <a class=" btn btn-secondary mx-3" href="{% url 'accounts:userlist' %}" role="button">Back</a>
  </div>
{% else %}
  <div class="d-flex justify-content-end">
    <a class=" btn btn-secondary mx-3" href="{% url 'accounts:userlist' %}" role="button">Back</a>
  </div>
{% endif %}

<!-- update.html -->
% extends 'base.html' %}
{% block content %}
  {% load django_bootstrap5 %}
  <div class="container d-flex justify-content-center py-5">
    <div class="card col-6 review-detail">
        {% comment %} <div class="review-detail rounded-4 shadow-lg p-5"> {% endcomment %}
      <h1 class="text-center mt-5 mb-3 fs-3 fw-bold text-white">Edit Profile</h1>
      <div class="card-body">
        <form action="{% url 'accounts:update' %}" method="POST" class="text-dark px-5 py-3">
          {% csrf_token %}
          {% bootstrap_field form.email %}
          {% bootstrap_field form.first_name %}
          {% bootstrap_field form.last_name %}
          <div class="text-end mt-4">
            <input type="submit" class="btn btn-warning" value="Save">
            <a class=" btn btn-dark ms-3" href="{% url 'accounts:profile' user.pk %}" role="button">Back</a>
          </div>
        </form>
      </div>
    </div>
  </div>
{% endblock content %}
```

<hr>


<br>

### Change Password 페이지

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197584975-8307f512-9911-4858-a01b-b5faf4bb985a.jpeg" alt="changepassword"  /></p>

- Profile 페이지에서 `Change Password`를 클릭하면, 비밀번호 변경 폼이 나오게 된다.

```python
# urls.py
from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
  path("password/", views.change_password, name="change_password"),
]
```

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("articles:index")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)
```

```html
<!-- change_password.html -->
% extends 'base.html' %}
{% block content %}
  {% load django_bootstrap5 %}

  <div class="container d-flex justify-content-center py-5">
    <div class="card col-6 review-detail">
      <h1 class="text-center mt-5 mb-3 fs-3 fw-bold text-white">Reset Password</h1>
      <div class="card-body">
        <form action="{% url 'accounts:update' %}" method="POST" class="text-dark px-5 py-3">
            {% csrf_token %}
            {% bootstrap_form form %}
            <div class="text-end mt-4">
                <input type="submit" class="btn btn-warning" value="Save">
                <a class=" btn btn-dark ms-3" href="{% url 'accounts:profile' user.pk %}" role="button">Back</a>
            </div>
        </form>
      </div>
    </div>
  </div>

{% endblock content %}
```

<hr>


<br>

## Articles App

### Movie create 페이지

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197585035-a2dd1620-efb2-4c48-b934-ff07ab7c8988.png" alt="moviecreate"  /></p>

* 영화의 제목, 내용, 감독, 러닝타임(분), 개봉일을 선택 가능하다.
* 장르 또한 선택 가능하며, MultiselectField로 최대 3개까지 선택 가능하다.
* image와 Thumbnail 파일을 선택 할 수 있다. image파일은 영화 디테일 페이지에, Thumbnail은 글 썸네일에 쓰인다.

```python
# urls.py
from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
  path("movie/", views.movie, name="movie"),  # 영화 등록
]
```

```python
# views.py
from django.shortcuts import render, redirect
from .models import Movie
from .forms import ReviewForm

@login_required
def movie(request):
    if request.method == "POST":
        movie_form = MovieForm(request.POST, request.FILES)
        if movie_form.is_valid():
            movie = movie_form.save()
            return redirect("articles:index")
    else:
        movie_form = MovieForm()

    context = {
        "movie_form": movie_form,
    }

    return render(request, "articles/movie.html", context)
```

```html
<!-- movie.html -->
{% extends 'base.html' %}
{% load static %}
{% load django_bootstrap5 %}

{% block css %}{% endblock css %}

{% block content %}

  <div class="container d-flex justify-content-center py-5">
    <div class="card col-9 review-detail">
      <h1 class="text-center mt-5 fs-3 fw-bold text-white">Add Movie</h1>
      <div class="card-body">
        <form action="" method="POST" enctype="multipart/form-data" class="text-dark px-5 py-3">
          {% csrf_token %}
          {% bootstrap_form movie_form %}
          <div class="text-end mt-4">
            <input type="submit" class="btn btn-warning" value="Save">
            <a class=" btn btn-dark ms-3" href="{% url 'articles:index' %}" role="button">Back</a>
          </div>
        </form>
      </div>
    </div>
  </div>

{% endblock content %}
```

<hr>


<br>

### Index 페이지

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197584987-f9f0efd5-ea71-46ca-bef8-90dd906dde8f.jpeg" alt="index"  /></p>

* 모든 영화들을 확인 가능하며, 영화의 제목과 썸네일을 확인할 수 있다.
* 썸네일이 없는 영화는 기본 이미지를 출력한다.

```python
# urls.py
from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
  path("", views.index, name="index"),
]
```

```python
# views.py
from django.shortcuts import render, redirect
from .models import Review, Movie

def index(request):
    reviews = Review.objects.all()
    movies = Movie.objects.order_by("-pk")
    context = {
        "reviews": reviews,
        "movies": movies,
    }
    return render(request, "articles/index.html", context)
```

```html
<!-- index.html -->
{% extends 'base.html' %}
{% load static %}
{% block content %}

<div class="container text-center py-5">
  <h2 class="text-center mb-5 text-white">All Movies</h2>
  <div class="row g-4 g-sm-4 g-md-5 row-cols-1 row-cols-sm-2 row-cols-md-3">
    {% for movie in movies %}
    <div class="col mt-5 mb-4">
      <div class="card h-100 border border-5 border-warning shadow-lg">
        <a class="text-decoration-none" href="{% url 'articles:moviedetail' movie.pk %}">
          <h5 class="card-header fw-bold py-3 bg-black text-light">
            {{ movie.title }}
          </h5>
          {% if movie.thumbnail %}
          <div class="card-hover">
            <img src="{{ movie.thumbnail.url }}" class="card-img-top" alt="{{ movie.thumbnail }}">
          </div>
          {% else %}
          <div class="card-hover">
            <img src="{% static 'images/empty.jpg' %}" class="card-img-top" alt="...">
          </div>
          {% endif %}
        </a>
      </div>
    </div>
    {% endfor %}
  </div>
  <div class="d-flex justify-content-end mt-4 fixed-bottom">
    <a class="btn btn-warning m-5 fw-bold" href="{% url 'articles:movie' %}">Add Movie</a>
  </div>
</div>

{% endblock %}
```

---

<br>

### Moive detail 페이지

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197586300-6cc72da7-6b0d-4e11-b138-6383eaf15cea.png" alt="moviedetail"  /></p>

* 영화의 상세정보를 확인 가능하며, 리뷰 작성 및 리뷰 확인이 가능하다.
* `Back` 버튼을 누르면 index페이지로 돌아가게 된다
* 영화의 수정과 삭제가 가능하다.
* 작성한 리뷰들의 별점의 평점과 리뷰 수를 보여준다.
* 리뷰를 클릭해 `review detail` 페이지로 이동한다.

```python
# urls.py
from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
  path("movie/<int:movie_pk>", views.moviedetail, name="moviedetail"),
  path("<int:movie_pk>/movie_delete/", views.movie_delete, name="movie_delete"),  # 영화 삭제
]
```

```python
# views.py
from django.shortcuts import render, redirect
from .models import Review, Movie
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

# moviedetail
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

# movie_delete
@login_required
def movie_delete(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    movie.delete()
    return redirect("articles:index")
```

```html
<!-- moviedetail.html -->
{% extends 'base.html' %}
{% load static %}
{% load django_bootstrap5 %}

{% block css %}{% endblock css %}

{% block content %}
  <div class="container my-5">
    <div class="review-back py-1 px-5 rounded-4">
      <!-- movie image가 있는 경우 -->
      {% if movie.image %}
        <div class="d-flex justify-content-center">
          <img src="{{ movie.image.url }}" class="container">
        </div>
      {% endif %}
      <section class="my-5 d-flex justify-content-center">
        <div class="container mx-1">
          <div class="d-flex justify-content-between align-items-center">
            <h1 class="text-white fw-bolder m-0">{{ movie.title }}</h1>
            <div>
              <a class=" btn btn-outline-light m-2" href="{% url 'articles:movie_update' movie.pk %}">Edit</a>
              <a class=" btn btn-outline-danger m-2" href=" {% url 'articles:movie_delete' movie.pk %} ">Delete</a>
            </div>
          </div>
          <hr class=" mt-1 text-white">
          <p class="text-white">
            <span>평점
              <span class="text-warning fw-bold">{{ star }}</span>
              <span class="small">{{ avg }}({{ cnt }})</span>
            </span>
            <span>·</span>
            <span>{{ movie.jenre }}</span>
            <span>·</span>
            <span>{{ movie.runningtime }}분</span>
            <span>·</span>
            <span>감독 :
              {{ movie.director }}</span>
          </p>
          <p class="text-white">
            <span>개봉일 :
              {{ movie.releasedate }}</span>
          </p>
          <div class="d-flex">
            <div class="text-center me-5 my-2">
              <a class="p-0 btn btn-lg border-0 text-white" href="">
                <span class="bi bi-share fs-2"></span>
                <p class="small">Share</p>
              </a>
            </div>
            <div class="text-center me-4 my-2">
              <form action="{% url 'articles:likes' movie.pk %}" method="post">
                {% csrf_token %}
                {% if request.user in movie.like_users.all %}
                  <button type="submit" class="btn btn-none p-0 border-0">
                    <i class="bi bi-heart-fill fs-2 text-danger"></i>
                  </button>
                {% else %}
                  <button type="submit" class="btn btn-none p-0 border-0">
                    <i class="bi bi-heart fs-2 text-danger"></i>
                  </button>
                {% endif %}
              </form>
              <p class="small fs-6 text-white">Like(<span>{{ movie.like_users.all|length }}</span>)</p>
            </div>
          </div>
          <p class="text-white">{{ movie.summary }}</p>
        </div>
      </section>
    </div>
    <div class="d-flex justify-content-end mb-4 mt-5">
      <!-- 리뷰 추가 버튼 -->
      <a class="btn btn-warning" href="{% url 'articles:create' movie.pk %}">Add Review</a>
      <!-- index 페이지로 돌아가는 버튼 -->
      <a class="btn btn-dark ms-3" href="{% url 'articles:index' %}">Back</a>
    </div>
    <!-- 리뷰 페이지가 생성 되었을 때 -->
    {% if reviews %}
      <div class="review-back py-3 px-5 rounded-4">
        {% for review in reviews %}
          <div class="d-flex justify-content-between mt-5">
            <a class="text-white text-decoration-none" href="{% url 'articles:detail' review.pk %}">
              <h4 class="f">{{ review.title }}
              </h4>
              <span class="text-white fs-6">
                <i class="bi bi-star-fill text-warning"></i>
                {{ review.grade }}
              </span>
            </a>
            <a href="{% url 'articles:delete' review.pk %}" class="text-white small text-decoration-none">
              <i class="bi bi-x-lg"></i>
            </a>
          </div>
          <hr class="fw-bolder">
        {% endfor %}
      </div>
    {% endif %}
  </div>
</div>
{% endblock content %}
```

---

<br>

### Review create 페이지

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197586422-dd63f894-f77b-4237-abca-da8353da84ab.png" alt="reviewcreate"  /></p>

- `movie detail` 페이지에서 `add review`를 클릭하면 review 생성 폼을 페이지에 표시해준다
- 폼을 작성하여 제출 버튼을 누르면 moviedetail.html로 다시 돌아가 review를 index에 표시해준다

```python
# urls.py
from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
  path("<int:movie_pk>/create", views.create, name="create"),  # 리뷰 작성
]
```

```python
# views.py
from django.shortcuts import render, redirect
from .models import Movie
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

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
```

```html
<!-- create.html -->
{% extends 'base.html' %}
{% load static %}
{% load django_bootstrap5 %}

{% block css %}{% endblock css %}

{% block content %}
  <div class="container d-flex justify-content-center py-5">
    <div class="card col-9 review-detail">
      {% comment %} <div class="review-detail rounded-4 shadow-lg p-5"> {% endcomment %}
      <h1 class="text-center mt-5 mb-3 fs-3 fw-bold text-white">Review</h1>
      <div class="card-body">
        <form action="" method="POST" class="text-dark px-5 py-3">
          {% csrf_token %}
          {% bootstrap_form create_form %}
          <div class="text-end mt-4">
            <input type="submit" class="btn btn-warning" value="Save">
            {% comment %} <a class=" btn btn-dark ms-3" href="{% url 'articles:moviedetail' movie.pk %}" role="button">Back</a> {% endcomment %}
          </div>
        </form>
      </div>
      </div>
    </div>
{% endblock content %}

```

<hr>


<br>

### Review Update 페이지

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197586568-1e4d8d5c-a3e7-4e65-af7e-b10da0224a3d.jpeg" alt="reviewupdate"  /></p>

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197586578-d41343fd-5b22-4b87-a487-35ba874a9b36.png" alt="reviewupdate1"  /></p>

- review create를 하면 moviedetail.html에 리뷰가 표시된다.
- 각 리뷰를 클릭하면, 리뷰 상세 페이지로 이동하게 되는데, 이 때 리뷰 작성자의 겨우에만 `Edit` 버튼이 활성화 되고, 작성자가 아니면 edit버튼은 나오지 않는다.
- `Edit`버튼을 클릭하게 되면 리뷰 폼에 내가 작성한 리뷰 제목, 리뷰 내용, 평점이 나오게 된다.
- 폼을 모두 작성하고 `Save`버튼을 누르게 되면 다시 리뷰 상세페이지로 돌아가게 되고 수정된 내용이 반영되어 보여진다.

```python
# urls.py
from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
  path("<int:review_pk>/", views.detail, name="detail"), # 리뷰 보기
  path("<int:review_pk>/update", views.update, name="update"), # 리뷰 수정
]
```

```python
# views.py
from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm, CommentForm
from django.contrib.auth.decorators import login_required

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
```

```html
<!-- detail.html -->
{% extends 'base.html' %}
{% load static %}
{% load django_bootstrap5 %}
{% block css %}{% endblock css %}

{% block content %}
  <div class="container d-flex flex-column justify-content-center my-5">
    <div class="review-detail p-5 rounded-4 shadow-lg">
      <div class="d-flex justify-content-between">
      <h2 class="text-white font-space">{{ review.title }}</h2>
        {% if request.user == review.user %}
          <a href="{% url 'articles:update' review.pk %}" class="btn btn-outline-dark mt-5">Edit</a>
        {% endif %}
      </div>
      <i></i>
      <hr>
      <div class="d-flex justify-content-between align-middle">
        <p class="text-white">
          writer :
          {{ review.user }}</p>
        {% if review.created_at == review.updated_at %}
          <p class="text-white">{{ review.created_at }}</p>
        {% else %}
          <p class="text-white">{{ review.updated_at }}
            (수정됨)</p>
        {% endif %}
      </div>
      <hr class="mt-0">
      <pre class="fs-6 text-white ">{{ review.content }}</pre>
  ...
```

<hr>


### comments

<p align="center"><img src="https://user-images.githubusercontent.com/108653518/197584980-9f6f6e59-9ce8-4e05-8eac-1ece824cac8b.png" alt="comments"  /></p>

- review detail 페이지에서 댓글을 작성할 수 있다.
- 리뷰 아래에 placeholder로 "댓글을 남겨보세요 💬"라는 말이 있고, 우측 하단에 댓글 남기기 버튼이 있다.
- 아래에는 작성자와 작성 일자, 내용을 포함하는 댓글들과 댓글의 개수를 보여준다. 
- 자신이 작성한 댓글에만 삭제 버튼이 나타난다.

```python
# urls.py
from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
  path("<int:pk>/comments/", views.comment_create, name="comment_create"),  # 댓글 작성
  path(
    "<int:review_pk>/comments/<int:comment_pk>/delete/",
    views.comment_delete,
    name="comment_delete",
  ),  # 댓글 삭제
]
```

```python
# views.py
from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

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
```

```html
<!-- detail.html -->
...
	<hr>
  <form action="{% url 'articles:comment_create' review.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form %}
    <div class="text-end"><input class="btn btn-warning" type="submit" value="Comment"></div>
  </form>
  <h5 class="text-white">comments ({{ comments|length }})</h5>
  <hr>
  <ul class="list-group list-group-flush rounded-2">
    {% for comment in comments %}
    <li class="list-group-item align-middle">
      <div class="d-flex justify-content-between align-items-center">
        <p class="card-text text-muted m-2">{{ comment.user }}</p>
        <p class="card-text text-muted pt-3">{{ comment.created_at }}</p>

      </div>
      <div class="d-flex justify-content-between align-items-center m-2">
        <p class="">
          {{ comment.content }}
        </p>
        {% if request.user == comment.user %}
        <form action="{% url 'articles:comment_delete' review.pk comment.pk %}" method="POST">
          {% csrf_token %}
          <input class="text-danger bg-white ms-3 border-1 border-danger text-decoration-none rounded-2" type="submit" value="삭제">
        </form>
        {% endif %}
      </div>
    </li>
    {% endfor %}
  </ul>
  </div>
 </div>
{% endblock content %}
```

<hr>
<br>

