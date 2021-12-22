from django import forms


class ImageForm(forms.Form):
    profile_picture = forms.ImageField()
