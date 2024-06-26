from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from App_login.forms import CreteUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from App_login.models import UserProfile
from App_login.forms import EditProfile
from django.contrib.auth.decorators import login_required
from App_post.forms import PostForm
from django.contrib.auth.models import User
from App_login.models import Follow
# Create your views here.


def sign_up(request):
    form = CreteUserForm()
    registered = False
    if request.method == "POST":
        form = CreteUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse("App_login:login"))
    return render(
        request,
        "App_login/signup.html",
        context={"form": form, "title": "Sign Up", "registered": registered},
    )


def login_page(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("App_post:home"))
    return render(
        request, "App_login/login.html", context={"form": form, "title": "Login"}
    )


@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == "POST":
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse("App_login:profile"))
    return render(
        request,
        "App_login/edit_profile.html",
        context={"form": form, "title": "Edit Profile"},
    )

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy("App_login:login"))

@login_required
def profile(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse("App_post:home"))
    return render(request,'App_login/profile.html',context={'form':form})

@login_required
def user(request,username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user,following=user_other)
    if user_other == request.user:
        return HttpResponseRedirect(reverse("App_login:profile"))
    return render(request,'App_login/user_other.html',context={'user_other':user_other,'already_followed':already_followed})

@login_required
def follow(request,username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user,following=following_user)
    if not already_followed:
        followed_user = Follow(follower=follower_user,following=following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_login:user',kwargs={'username':username}))

@login_required
def unfollow(request,username):
     following_user = User.objects.get(username=username)
     follower_user = request.user
     already_followed = Follow.objects.filter(follower=follower_user,following=following_user)
     already_followed.delete()
     return HttpResponseRedirect(reverse('App_login:user',kwargs={'username':username}))
