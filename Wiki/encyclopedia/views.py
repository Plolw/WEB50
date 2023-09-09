from django.shortcuts import render
from . import util
from markdown2 import markdown
from . import util
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

class EntryForm(forms.Form):
    title = forms.CharField(label="title", max_length=20)
    content = forms.CharField(widget=forms.Textarea)
    

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
        "text": text,
        "title": title
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

def new_page(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return HttpResponse("Entry already exists")
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": EntryForm()
        })
    
def edit(request, x):
    if request.method  == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry"))
    else:
        text = util.get_entry(x)
        data = {'title': x, 'content': text}
        print(x)
        return render(request, "encyclopedia/edit.html", {
            "form": EntryForm(data),
            "title": x
        })

        
def edit(request,title):
    if request.method == "POST":
         return render(request, "encyclopedia/edit.html", {
            "form": EntryForm(request.POST)
        })
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": EntryForm(request.POST)
        })
