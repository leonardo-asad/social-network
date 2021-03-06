import json
from telnetlib import STATUS
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post
from .forms import PostForm


def index(request):

    # Get all posts ordered from the most recent to the oldest
    posts_all = Post.objects.all().order_by("-timestamp")

    # Use Paginator to paginate the querySet
    paginator = Paginator(posts_all, 10) # Shows 10 posts per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = Post(
                author=request.user,
                content=form.cleaned_data['content'],
                timestamp = timezone.now()
            )
            new_post.save()

            return HttpResponseRedirect(reverse("network:index"))

        else:
            return render(request, "network/index.html", {
                'posts': page_obj,
                'post_form': form
            })

    return render(request, "network/index.html", {
        'posts': page_obj,
        'post_form': PostForm()
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")

@login_required
def like_toogle(request, post_id):

    post = Post.objects.get(pk=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        action = 'unliked'
    else:
        post.likes.add(user)
        action = 'liked'

    data = {
        'action': action,
        'likes': post.likes.all().count(),
        'post_id': str(post.pk)
    }

    return JsonResponse(data, status=200)


def profile(request, user_id):

    user_profile = User.objects.get(pk=user_id)

    posts_all = Post.objects.filter(author=user_profile).all().order_by("-timestamp")

    # Use Paginator to paginate the querySet
    paginator = Paginator(posts_all, 10) # Shows 10 posts per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        'user_profile': user_profile,
        'posts': page_obj
    })

@login_required
def follow_toogle(request, user_id):

    user_profile = User.objects.get(pk=user_id)

    if user_profile in request.user.following.all():
        request.user.following.remove(user_profile)
        action = "unfollowed"
    else:
        request.user.following.add(user_profile)
        action = "followed"

    data = {
        'action': action,
        'following': user_profile.following.all().count(),
        'followers': user_profile.followers.all().count()
    }
    return JsonResponse(data, status=200)

@login_required
def following(request):

    following_users = request.user.following.all()

    all_posts = Post.objects.all()

    filtered_posts = [post for post in all_posts if post.author in following_users]

    return render(request, "network/following.html", {
        'posts': filtered_posts
    })

@csrf_exempt
def edit(request, post_id):

    post = Post.objects.get(pk=post_id)

    # If the request is not made by the author of the post, it is denied
    if not post.author == request.user:
        return HttpResponse(status=403)

    if request.method == "POST":

        data = json.loads(request.body)

        # Update the content of the post
        post.content = data.get('content')
        post.save(update_fields=['content'])

        #breakpoint()

        return HttpResponse(status=200)


    return JsonResponse({'post_content': post.content}, status=200)
