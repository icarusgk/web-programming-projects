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
    comment_input = forms.CharField(widget=forms.Textarea(
        attrs={"rows": 5, "cols": 20}), label='')


class BidForm(forms.Form):
    new_bid = forms.FloatField()
