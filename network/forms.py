from .models import Post
from django import forms

class PostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'3'}))
