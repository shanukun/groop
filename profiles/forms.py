from django import forms

from .models import Profile


class ProfileModelForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    bio = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2})
    )

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "bio", "avatar")
