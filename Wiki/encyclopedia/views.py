from django.shortcuts import render
from . import util
from django.http import HttpResponse
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random as rd

entries = util.list_entries()
results = []
chars = []
clean_data = ""

# Index and Layout Page

def index(request):
	return render(request, "encyclopedia/index.html", {
    "entries": entries
  })

# Page Content

def content(request, name):
  if name in util.list_entries():
    return render(request, "encyclopedia/content.html", {
    	"page_content": util.convert(name),
			"name": name,
			"md_content": util.get_entry(name)
    })
  else:
  	return render(request, "encyclopedia/not_found.html", {
			"page_name": name
		})

# Search

def search(request):
	"""
	Searches along the entries to determine if 
	the requested query exists.
	"""
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
				"query": query
			})

def create(request):
	return render(request, "encyclopedia/create.html")

def create_entry(request):
	"""
	Creates a new entry for the wiki
	"""

	if request.method == "GET":
		new_entry = request.GET.get('new_entry', '')
		title = request.GET.get('title', '')

		if new_entry.__len__() == 0:
			return render(request, "encyclopedia/empty.html")

		if new_entry and title:
			if title in entries:
				return render(request, "encyclopedia/error.html", {
					"name": title
				})
			else:
				util.save_entry(title, new_entry)
				entries.append(title)		

		return render(request, "encyclopedia/content.html", {
			"page_content": util.convert(title),
			"name": title,
			"md_content": new_entry
		})

# Edit 

def edit(request):
	if request.method == "GET":
		title = request.GET.get('entry', '')
		content = request.GET.get('entry_text', '')

	return render(request, "encyclopedia/edit.html", {
		"title": title,
		"content": content
	})

def edit_page(request):
	"""
	Given a page name, it returns the page to edit
	"""
	if request.method == "GET":
		updated_title = request.GET.get('edit_title', '')
		updated_content = request.GET.get('edit_text', '')

		util.save_entry(updated_title, updated_content)

		return render(request, "encyclopedia/content.html", {
			"page_content": util.convert(updated_title),
			"name": updated_title,
			"md_content": updated_content 
		})

# Random

def random(request):
	"""
	Given the entries, returns a random one
	"""
	n_page = rd.randint(0, entries.__len__()-1)
	page = entries[n_page]

	return render(request, "encyclopedia/content.html",{
		"page_content": util.convert(page),
		"name": page,
		"md_content": util.get_entry(page)
	})