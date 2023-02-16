from django import forms

from .models import Comment, Post


class PostModelForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2})
    )
    # image = forms.ImageField(
    #         widget=forms.FileInput(attrs={"class": "form-control form-control-sm", "novalidate": True})
    # )

    class Meta:
        model = Post
        fields = ("content", "image")


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "add a comment..."}
        ),
    )

    class Meta:
        model = Comment
        fields = ("body",)
