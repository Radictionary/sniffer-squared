import os
from django.http import HttpResponseNotAllowed, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings


from django.contrib.auth import get_user_model, authenticate, logout

from asgiref.sync import async_to_sync, sync_to_async


from .backend import (
    shutdown,
    start,
    send_notification,
    run_file_status,
    get_history,
    add_to_whitelist,
    remove_from_whitelist,
    add_to_blacklist,
    remove_from_blacklist,
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

import asyncio

@sync_to_async
@login_required
@async_to_sync
async def history_view(request):
    try:
        history = await asyncio.wait_for(get_history(), timeout=2)
    except TimeoutError:
        history = {}
    
    return render(
        request,
        "history.html",
        context=make_context(
            title="Network History",
            **history,
        )
    )

# json version of history view
@sync_to_async
@login_required
@async_to_sync
async def history_view_json(request):
    try:
        history = await asyncio.wait_for(get_history(), timeout=2)
    except TimeoutError:
        history = {}
    
    return render(
        request,
        "history_update.html",
        context=make_context(
            title="Network History",
            **history,
        )
    )


from django.http import JsonResponse

# add to whitelist GET/POST endpoint
async def add_to_whitelist_view(request):
    if request.method == "GET" or request.method == "POST":
        if request.method == "POST":
            print("----------------- REQUEST.POST DICTIONARY -----------------")
            print(request.POST)
            ip = request.POST.get("ip")
            if not ip:
                # 400 error
                return JsonResponse({"error": "No IP provided."}, status=400)
        else:
            ip = request.GET.get("ip")
            if not ip:
                # 400 error
                return JsonResponse({"error": "No IP provided."}, status=400)
        
        print("IP: --------------------------------------------------- ", ip)
        data = await add_to_whitelist(ip)
        send_notification(
            "Whitelist Update",
            f"Added {ip} to the whitelist."
        )
        print(f"-------------------------------------------------- SENDING DATA: {data}")
        return JsonResponse(data)
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

# remove from whitelist GET/POST endpoint
async def remove_from_whitelist_view(request):
    if request.method == "GET" or request.method == "POST":
        if request.method == "POST":
            ip = request.POST.get("ip")
            if not ip:
                # 400 error
                return JsonResponse({"error": "No IP provided."}, status=400)
        else:
            ip = request.GET.get("ip")
            if not ip:
                # 400 error
                return JsonResponse({"error": "No IP provided."}, status=400)
        
        print("IP: --------------------------------------------------- ", ip)
        
        data = await remove_from_whitelist(ip)
        send_notification(
            "Whitelist Update",
            f"Removed {ip} from the whitelist."
        )
        return JsonResponse(data)
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

# add to blacklist GET/POST endpoint
async def add_to_blacklist_view(request):
    if request.method == "GET" or request.method == "POST":
        if request.method == "POST":
            ip = request.POST.get("ip")
            if not ip:
                # 400 error
                return JsonResponse({"error": "No IP provided."}, status=400)
        else:
            ip = request.GET.get("ip")
            if not ip:
                # 400 error
                return JsonResponse({"error": "No IP provided."}, status=400)
        
        print("IP: --------------------------------------------------- ", ip)
        data = await add_to_blacklist(ip)
        send_notification(
            "Blacklist Update",
            f"Added {ip} to the blacklist."
        )
        return JsonResponse(data)
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

# remove from blacklist GET/POST endpoint
async def remove_from_blacklist_view(request):
    if request.method == "GET" or request.method == "POST":
        if request.method == "POST":
            ip = request.POST.get("ip")
            if not ip:
                # 400 error
                return JsonResponse({"error": "No IP provided."}, status=400)
        else:
            ip = request.GET.get("ip")
            if not ip:
                # 400 error
                return JsonResponse({"error": "No IP provided."}, status=400)
        
        print("IP: --------------------------------------------------- ", ip)
        data = await remove_from_blacklist(ip)
        send_notification(
            "Blacklist Update",
            f"Removed {ip} from the blacklist."
        )
        return JsonResponse(data)
    else:
        return HttpResponseNotAllowed(["GET", "POST"])

@login_required
def about(request):
    return render(request, "about.html", context=make_context(title="About"))


@only_on_startup
def create_super_user_view(request):
    if request.method == "POST":
        User = get_user_model()
        send_notification(
            "Superuser created.", 
           f"A superuser named {request.POST['username']} has been created."
            "Superuser created.",
            f"A superuser named {request.POST['username']} has been created.",
        )
        User.objects.create_superuser(
            username=request.POST["username"],
            password=request.POST["password"],
            email=request.POST["email"],
        )
        authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        return redirect("/")
    elif request.method == "GET":
        return render(
            request,
            "create_superuser.html",
            context=make_context(title="Create Superuser"),
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
        ),
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")


# @login_required
# def history(request):
#     return render(
#         request,
#         "history.html",
#         context=make_context(title="Your History")
#     )

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
    # favicon not included here
    ('', index), 
    ('history/', history_view),
    ('shutdown/', shutdown_view),
    ('start/', start_view),
    ('create_superuser/', create_super_user_view),
    ('accounts/profile/', redirect_to_index),
    ('about/', about),
    ('logout/', logout_view),
    # whitelist
    ('whitelist/add/', add_to_whitelist_view),
    ('whitelist/remove/', remove_from_whitelist_view),
    # blacklist
    ('blacklist/add/', add_to_blacklist_view),
    ('blacklist/remove/', remove_from_blacklist_view),
    # ('favicon.ico', favicon),
    ('history/json/', history_view_json),
]
