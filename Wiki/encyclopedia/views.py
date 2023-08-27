from django.shortcuts import render
from . import util
from markdown2 import markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/entry.html", {
        "text": "<h1>Page not found</h1>"
    })
    text = markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "text": text
    })


def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        q = request.POST["q"]
        if util.get_entry(q) != None:
            return render(request, "encyclopedia/entry.html", {
                "text": markdown(util.get_entry(q))
            })
        results = []
        for entry in entries:
            if q.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/search.html", {
        "entries": results
    })
    return render(request, "encyclopedia/search.html", {
        "entries": util.list_entries()
    })
