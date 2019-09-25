from django import forms

class NameForm(forms.Form):
    amount = forms.IntegerField(label='Montant')