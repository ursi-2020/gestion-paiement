from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='Name for article', max_length=100)