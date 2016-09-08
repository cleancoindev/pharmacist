from django import forms

class MedicationForm(forms.Form):
    quantity_to_dispense = forms.ChoiceField(choices=[(i, i) for i in range(1, 1024)])
