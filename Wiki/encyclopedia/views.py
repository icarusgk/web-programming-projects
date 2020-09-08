from django.shortcuts import render
from . import util
from django.http import HttpResponse

# pages = ["/entries/CSS.md"]

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    return render(request, "encyclopedia/create.html")

def random(request):
    return render(request, "encyclopedia/random.html")

def content(request, name):
    if name in util.list_entries():
        return render(request, "encyclopedia/content.html", {
            "page_content": util.convert(util.get_entry(name))
        })
    else:
        return render(request, "encyclopedia/not_found.html")

# def link(request, place_name):

