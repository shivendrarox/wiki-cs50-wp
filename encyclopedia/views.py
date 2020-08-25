from django.shortcuts import render
from django.http import HttpResponse
#from django.urls import resolve
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django import forms


import markdown2
from . import util
import random




class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Entry Title")
    entry_body = forms.CharField(label="Entry Content",widget=forms.Textarea())


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def call_get_entry(request,entry_name):
    try:
        mhtml = markdown2.markdown(util.get_entry(entry_name))
    except TypeError:
        mhtml="<h1>Whoops! No such entry</h1>"

    return render(request, "encyclopedia/layout.html", {
        "entry":mhtml,
        "ename":entry_name,
        "editable":True
    })


def show_entry(request):
    entry_name=request.GET.get('q')
    entry_list = util.list_entries()
    print(entry_name)
    print(entry_list)
    result_list=[]
    for e in range(len(entry_list)):
        if entry_list[e].casefold().startswith(entry_name.casefold()):
            print("match found")
            result_list.append(entry_list[e])

    print(result_list)
    entry_exists=True
    try:
        mhtml = markdown2.markdown(util.get_entry(entry_name))
    except TypeError:
        entry_exists=False
        mhtml="<h1>Whoops! No such entry</h1>"

    if result_list == [] :
        return render(request, "encyclopedia/layout.html", {
        "entry":mhtml
    })
    if entry_exists:
        rd_url = "/wiki/"+entry_name
        print(rd_url)
        return redirect(rd_url)
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": result_list
    })

    rd_url = "/wiki/"+entry_name
    print(rd_url)
    return redirect(rd_url)

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"]
            entry_body = form.cleaned_data["entry_body"]
            if entry_title in util.list_entries():
                return render(request, "encyclopedia/layout.html", {
                        "entry":"<h1>Sorry, Entry Already Exists!!!<h1>"
                        })
            
            util.save_entry(entry_title,entry_body)

            r_url = "/wiki/"+entry_title
            return HttpResponseRedirect(r_url)
        else:
            return render(request,"encyclopedia/layout.html",{
                "form" : form
            })

    return render(request,"encyclopedia/layout.html",{
        "form":NewEntryForm(),
    })


class EditForm(forms.Form):
    title = forms.CharField(label="Title",disabled=False)
    body = forms.CharField(label="Content",widget=forms.Textarea)


def edit_page(request,entry_name):
    if request.method == "POST":
        form = EditForm(request.POST)

        #if form.is_valid(): we are not validatiing
        entry_title = entry_name#form.cleaned_data["title"] no clean data availabe
        entry_body = form['body'].value()#form.cleaned_data["body"] no clean data available

        util.save_entry(entry_title,entry_body)

        r_url = "/wiki/"+entry_title
        return HttpResponseRedirect(r_url)

    return render(request,"encyclopedia/layout.html",{
        "form":None,
        "edit_form":True,
        "ename":entry_name,
        "ebody":util.get_entry(entry_name)
    })

def random_page(request):
    entries_list=util.list_entries()
    print(entries_list)
    r_entry = random.choice(entries_list)
    print("random item from list is: ", r_entry )

    rd_url="/wiki/"+r_entry
    return HttpResponseRedirect(rd_url)
