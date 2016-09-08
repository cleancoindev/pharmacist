import requests, urllib
from email import send_refill_email
from models import Patient, Medication, AuditLog


class DrchronoAPI:
    def __init__(self, user):
        access_token = user.social_auth.get(user=user).extra_data['access_token']
        self.headers = {'Authorization': 'Bearer {0}'.format(access_token)}

    def _get_all_patients(self):
        url = 'https://drchrono.com/api/patients'

        # Fetch the objects one "page" at a time until they are all loaded
        while url:
            data = requests.get(url, headers=self.headers).json()
            for item in data['results']:
                Patient().save_from_dict(item)
            url = data['next']      # Value = None on the last page

    def _get_all_medications(self):
        url = 'https://drchrono.com/api/medications'
        while url:
            data = requests.get(url, headers=self.headers).json()
            for item in data['results']:
                Medication().save_from_dict(item)
            url = data['next']

    def update(self):
        if not Patient.objects.exists():
            self._get_all_patients()
        if not Medication.objects.exists():
            self._get_all_medications()

    def patch(self, user, endpoint, item_id, parameters):
        if item_id:
            url = 'https://drchrono.com/api/{0}/{1}'.format(endpoint, item_id)
        else:
            url = 'https://drchrono.com/api/{0}'.format(endpoint)
        data = requests.patch(url, headers=self.headers, data=parameters).text
        return data

def dispense_med(user, form, med_id, qty):
    med = Medication.objects.get(item_id=med_id)
    patient = med.patient

    # You can't PATCH a medication over the API, so can't actually update the refills but we'll store it locally
    med.number_refills = max([med.number_refills - qty, 0])
    med.save()

    log_text = 'dispensed {0} x {1} to {2} {3}'.format(qty, med.name, patient.first_name, patient.last_name)
    AuditLog(user=user, text=log_text).save()

    # If the remaining refills drops below 2, send a reminder email
    if med.number_refills < 2:
        send_refill_email(patient, med)
        log_text = 'sent reminder email to {0} {1} at {2}'.format(patient.first_name, patient.last_name, patient.email)
        AuditLog(user=user, text=log_text).save()
