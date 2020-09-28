from django import forms
from .models import Category

class ListingForm(forms.Form):
    title = forms.CharField(max_length=256)
    description = forms.CharField(widget=forms.Textarea)
    image_url = forms.URLField()
    category = forms.CheckboxInput()
