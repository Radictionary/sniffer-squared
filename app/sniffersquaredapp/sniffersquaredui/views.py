from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(
        request,
        "index.html",
        context=dict(title="Your Console")
    )

@login_required
def history(request):
    return render(
        request,
        "history.html",
        context=dict(title="Your History")
    )

routes = [
    ('', index), 
    ('history/', history)
]