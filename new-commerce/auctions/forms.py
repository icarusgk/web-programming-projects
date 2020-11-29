from django import forms
from .models import Category


class ListingForm(forms.Form):
    CHOICES = Category.objects.values_list()

    title = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': "Enter your product's title here", 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}))
    image_url = forms.URLField(widget=forms.TextInput(attrs={'placeholder': "Enter your product's image URL here", 'class': 'form-control'}))
    bid = forms.FloatField()
    category = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CHOICES
    )


class CommentForm(forms.Form):
    comment_input = forms.CharField(widget=forms.Textarea(
        attrs={"rows": 5, "cols": 20}), label='')


class BidForm(forms.Form):
    new_bid = forms.FloatField()
