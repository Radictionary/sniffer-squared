from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .backend import shutdown, start

# Create your views here.

default_context = dict(
    nav_items=[
        {"url": "/", "title": "Console"},
        {"url": "/history/", "title": "History"},
        {"url": "/shutdown/", "title": "Shutdown"},
        {"url": "/start/", "title": "Start"},
    ],
)

def make_context(**kwargs):
    return default_context | kwargs

@login_required
def index(request):
    return render(
        request,
        "index.html",
        context=make_context(title="Your Console")
    )

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

routes = [
    ('', index), 
    ('history/', history),
    ('shutdown/', shutdown_view),
    ('start/', start_view),
]