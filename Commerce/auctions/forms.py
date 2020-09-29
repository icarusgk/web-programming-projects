from django import forms
from .models import Category

class ListingForm(forms.Form):
    CHOICES = Category.objects.values_list()

    title = forms.CharField(max_length=256)
    description = forms.CharField(widget=forms.Textarea)
    image_url = forms.URLField()
    bid = forms.FloatField()
    category = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CHOICES
    )

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, max_length=256)


    