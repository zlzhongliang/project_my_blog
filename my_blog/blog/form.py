from django import forms
from ckeditor.widgets import CKEditorWidget

class RegisterForm(forms.Form):
    email = forms.CharField(widget=forms.Textarea)
    password = forms.IntegerField()



