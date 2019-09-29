from django import forms

class NameForm(forms.Form):
    amount = forms.DecimalField(label='Montant')