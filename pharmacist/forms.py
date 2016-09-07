from django import forms

class MedicationForm(forms.Form):
    quantity_to_dispense = forms.ChoiceField(choices=[(x, x) for x in range(1, 3)])
