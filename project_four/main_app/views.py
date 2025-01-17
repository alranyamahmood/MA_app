from django.shortcuts import render, redirect
# Add the following import
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Post, Profile, Comment
from .forms import PostForm
# from .models import User


# Add the following import
from django.http import HttpResponse

# views.py
from django.views.generic import ListView

# Define the home view


def home(request):
    return render(request, 'home.html')


def se(request):
    return render(request, 'se.html')


class PostCreate(CreateView):
    model = Post
    fields = ['topic', 'lesson']
    success_url = '/'

    def form_valid(self, form):
        # Assign the logged in user
        form.instance.upvotes = 0
        form.instance.downvotes = 0
        form.instance.updates = ''
        form.instance.user = self.request.user
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super(PostCreate, self).form_valid(form)


def signup(request):
    context = {"error": False}
    if request.method == "GET":
        return render(request, 'main_app/signup.html', context)
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["password"]
        try:
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username,
                password=password, email=email)
            if user is not None:
                # run the login method to automatically log in user
                # as they sign up.
                return signin(request)
        except:
            context["error"] = f"Username '{username}' already exists."
            return render(request, 'main_app/signup.html', context)


def signin(request):
    context = {"error": False}
    if request.method == "GET":
        return render(request, 'main_app/signin.html')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')


def signout(request):
    auth.logout(request)
    return redirect('/')
