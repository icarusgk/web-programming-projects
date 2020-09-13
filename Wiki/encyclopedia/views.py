from django.shortcuts import render
from . import util
from django.http import HttpResponse
from django import forms
from django.urls import reverse


entries = util.list_entries()

# Index and Layout Page

def index(request):
	return render(request, "encyclopedia/index.html", {
    "entries": entries,
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
n_results = 0

# Search


def search(request):
	if request.method == "GET":
		query = request.GET.get('q', '')
		
		for char in query:
			chars.append(char)
		
		results.clear()
		
		if chars.__len__() > 0:
			for entry in entries:
				clean_data = entry.upper()

				if chars[0].upper() in clean_data:
					results.append(entry)
					n_results = results.__len__()
		
		chars.clear()

		if query in entries:
			return render(request, "encyclopedia/content.html", {
				"page_content": util.convert(query)
			})
		elif query == '':
			return render(request, "encyclopedia/index.html", {
				"entries": entries
			})
		elif query not in entries:
			return render(request, "encyclopedia/results.html", {
				"results": results,
				"entries": entries,
				"query": query,
				"number_of_results": n_results
			})

def create(request):
	return render(request, "encyclopedia/create.html", {
		"page_content": util.convert("Git")
	})