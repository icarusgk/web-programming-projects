from django.shortcuts import render
from . import util
from django.http import HttpResponse
from django import forms
from django.urls import reverse

class SearchEntry(forms.Form):
	query = forms.CharField(label="Search:")


entries = util.list_entries()

# Index and Layout Page

def index(request):

	if request.method == "POST":
		form = SearchEntry(request.POST)

		if form.is_valid():
			query = form.cleaned_data["value"]
			if query in entries:
				return render(request, "encyclopedia/content.html", {
					"page_content": util.convert(query)
				})
			else:
				return render(request, "encyclopedia/not_found.html",{
					"form": form,
					"page_name": query
				})

	return render(request, "encyclopedia/index.html", {
    "entries": entries,
		"form": SearchEntry()
  })

# Page Content
def content(request, name):
  if name in util.list_entries():
    return render(request, "encyclopedia/content.html", {
      "page_content": util.convert(name)
    })
  else:
  	return render(request, "encyclopedia/not_found.html", {
			"page_name": name
		})


results = []
chars = []
clean_data = ""
# Search
def search(request):
	if request.method == "GET":
		query = request.GET.get('q', '')
		
		for char in query:
			chars.append(char)

		for entry in entries:
			clean_data = entry.upper()
			if chars[0].upper() in clean_data:
				results.append(clean_data)

		if query in entries:
			return render(request, "encyclopedia/content.html", {
				"page_content": util.convert(query)
			})
		elif query in clean_data:
			return render(request, "encyclopedia/results.html", {
				"results": results,
				"entries": entries
			})
		elif query == '':
			return render(request, "encyclopedia/index.html", {
				"entries": entries
			})
		else:
			return render(request, "encyclopedia/not_found.html",{
				"page_name": query
			})
				
