from django import forms
from localflavor.us.forms import USSocialSecurityNumberField


class PatientAuthForm(forms.Form):
    ssn = USSocialSecurityNumberField(label="Social Security Number")

class MedicationForm(forms.Form):
    quantity_to_dispense = forms.ChoiceField(choices=[(i, i) for i in range(1, 1024)])
