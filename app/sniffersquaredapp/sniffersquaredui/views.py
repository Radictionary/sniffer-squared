from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model, authenticate, logout

from .backend import (
    shutdown, 
    start, 
    send_notification,
    run_file_status,
)

from functools import wraps

# possible upgrades:
# - page for about.html rejecting the request because users already exist.

default_context = dict(
    nav_items=[
        {"url": "/", "title": "Dashboard"},
        {"url": "/history/", "title": "History"},
        {"url": "/shutdown/", "title": "Shutdown"},
        {"url": "/start/", "title": "Start"},
        {"url": "/about/", "title": "About"},
    ],
)

def make_context(**kwargs):
    return default_context | kwargs

def favicon(_):
    return redirect("/static/favicon.ico")

def no_users_exist():
    User = get_user_model()
    return User.objects.count() == 0

def only_on_startup(func):
    @wraps(func)
    def wrapper(request):
        if no_users_exist():
            return func(request)
        else:
            return redirect("/")
    return wrapper

@login_required
def about(request):
    return render(
        request,
        "about.html",
        context=make_context(title="About")
    )

@only_on_startup
def create_super_user_view(request):
    if request.method == "POST":
        User = get_user_model()
        send_notification(
            "Superuser created.", 
            f"A superuser named {request.POST['username']} has been created."
        )
        User.objects.create_superuser(
            username=request.POST["username"],
            password=request.POST["password"],
            email=request.POST["email"]
        )
        authenticate(request, 
                     username=request.POST['username'], 
                     password=request.POST["password"]
        )
        return redirect("/")
    elif request.method == "GET":
        return render(
            request,
            "create_superuser.html",
            context=make_context(title="Create Superuser")
        )
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

def index(request):
    if no_users_exist():
        return redirect("/create_superuser/")
    
    # require login
    if not request.user.is_authenticated:
        return redirect("/accounts/login/?next=/")

    return render(
        request,
        "index.html",
        context=make_context(
            title="Your Console", 
            run_file_status=run_file_status(),
            email=request.user.email,
            name=request.user.username,
        )
    )

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")


@login_required
def history(request):
    return render(
        request,
        "history.html",
        context=make_context(title="Your History")
    )

@login_required
def shutdown_view(request):
    shutdown()
    return redirect("/")

@login_required
def start_view(request):
    start()
    return redirect("/")

def redirect_to_index(request):
    return redirect("/")

routes = [
    ('', index), 
    ('history/', history),
    ('shutdown/', shutdown_view),
    ('start/', start_view),
    ('create_superuser/', create_super_user_view),
    ('accounts/profile/', redirect_to_index),
    ('about/', about),
    ('logout/', logout_view),
    # ('favicon.ico', favicon),
]