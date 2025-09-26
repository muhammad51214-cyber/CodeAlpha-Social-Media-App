from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .models import Post, Comment, Like, Follow
from .forms import PostForm, CommentForm, SignupForm

def signup(request):
    if request.user.is_authenticated:
        return redirect("feed")
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("feed")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def feed(request):
    following_ids = Follow.following_ids_for(request.user)
    posts = (
        Post.objects.filter(Q(author=request.user) | Q(author__in=following_ids))
        .select_related("author")
        .prefetch_related("comments__author", "likes")
    )
    post_form = PostForm()
    return render(request, "feed.html", {"posts": posts, "post_form": post_form})

@login_required
def post_create(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
    return redirect("feed")

def post_detail(request, pk: int):
    post = get_object_or_404(Post.objects.select_related("author").prefetch_related("comments__author", "likes"), pk=pk)
    comment_form = CommentForm()
    return render(request, "post_detail.html", {"post": post, "comment_form": comment_form})

@login_required
def comment_create(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("post_detail", pk=pk)

@login_required
def like_toggle(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    # Redirect back to referring page if available
    next_url = request.META.get("HTTP_REFERER")
    return redirect(next_url or "feed")

def _get_user_by_username(username: str) -> User:
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User not found")

def profile_detail(request, username: str):
    profile_user = _get_user_by_username(username)
    posts = profile_user.posts.all().select_related("author").prefetch_related("likes")
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    return render(request, "profile_detail.html", {"profile_user": profile_user, "posts": posts, "is_following": is_following})

@login_required
def follow_toggle(request, username: str):
    target = _get_user_by_username(username)
    if target == request.user:
        return HttpResponseBadRequest("Cannot follow yourself")
    rel, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        rel.delete()
    next_url = request.META.get("HTTP_REFERER")
    return redirect(next_url or "profile_detail", username=username)