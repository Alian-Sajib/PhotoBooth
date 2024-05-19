from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from App_login.models import Follow
from App_post.models import Post, Like


# Create your views here.
@login_required
def home(request):
    following_list = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=following_list.values_list("following"))
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list("post", flat=True)
    print(liked_post_list)
    if request.method == "GET":
        # Getting the search value. Adding space for contains use in next line
        search = request.GET.get("Search", "")
        # Search portion wise and using i for case sensitive search
        result = User.objects.filter(username__icontains=search)

    return render(
        request,
        "App_post/home.html",
        context={
            "title": "Home",
            "result": result,
            "search": search,
            "posts": posts,
            "liked_post_list": liked_post_list,
        },
    )


@login_required
def liked(request, pk):
    post = Post.objects.get(pk=pk)
    already_like = Like.objects.filter(post=post, user=request.user)
    if not already_like:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
    return HttpResponseRedirect(reverse("App_post:home"))


@login_required
def unliked(request, pk):
    post = Post.objects.get(pk=pk)
    already_like = Like.objects.filter(post=post, user=request.user)
    already_like.delete()
    return HttpResponseRedirect(reverse("App_post:home"))
