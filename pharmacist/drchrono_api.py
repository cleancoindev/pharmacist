import requests, urllib
from email import send_refill_email
from models import Patient, Medication, AuditLog


class DrchronoAPI:
    def __init__(self, user):
        access_token = user.social_auth.get(user=user).extra_data['access_token']
        self.headers = {'Authorization': 'Bearer {0}'.format(access_token)}

    def update(self):
        if not Patient.objects.exists():
            self._get_all_patients()
        if not Medication.objects.exists():
            self._get_all_medications()

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


endpoint_models = {
    'patients': Patient,
    'medications': Medication,
    }


def get_one(user, endpoint, item_id, parameters={}):
    # First, try to retrieve data from our DB if we've retrieved it from the API previously
    model = endpoint_models[endpoint]
    try:
        data = model.objects.get(item_id=item_id, **parameters)
    except:
        # Get it from the API directly
        # TODO: wrap this in an error-handler / logger
        social = user.social_auth.get(user=user)
        access_token = social.extra_data['access_token']
        headers = {'Authorization': 'Bearer {0}'.format(access_token)}
        url = 'https://drchrono.com/api/{0}/{1}?{2}'.format(endpoint, item_id, urllib.urlencode(parameters))
        data = requests.get(url, headers=headers).json()

        # Save the item in the DB for future reference
        new_model = model()
        new_model.save_from_dict(data)
        return new_model

    return data

def get_all(user, endpoint, parameters={}, patient=None):
    # Try the DB first for data
    model = endpoint_models[endpoint]

    all_objs = model.objects
    if patient:
        patient = Patient.objects.get(item_id=patient)
        all_objs = all_objs.filter(patient=patient)

    if not all_objs.exists():
        all_objs = []
        # Get it from the API directly
        # TODO: wrap this in an error-handler / logger
        social = user.social_auth.get(user=user)
        access_token = social.extra_data['access_token']
        headers = {'Authorization': 'Bearer {0}'.format(access_token)}
        url = 'https://drchrono.com/api/{0}?{1}'.format(endpoint, urllib.urlencode(parameters))
        json_objs = []

        # Fetch the objects one "page" at a time
        while url:
            data = requests.get(url, headers=headers).json()
            json_objs.extend(data['results'])
            url = data['next'] # A JSON null on the last page

        for item in json_objs:
            new_model = model()
            new_model.save_from_dict(item)
            all_objs.append(new_model)

    return all_objs

def update(user, endpoint, item_id, parameters):
    social = user.social_auth.get(user=user)
    access_token = social.extra_data['access_token']
    headers = {'Authorization': 'Bearer {0}'.format(access_token)}
    if item_id:
        url = 'https://drchrono.com/api/{0}/{1}'.format(endpoint, item_id)
    else:
        url = 'https://drchrono.com/api/{0}'.format(endpoint)
    data = requests.patch(url, headers=headers, data=parameters).text
    return data

def dispense_med(user, form, med_id, qty):
    #med = get_one(user, 'medications', med_id)
    #patient = get_one(user, 'patients', med.patient.item_id)

    med = Medication.objects.get(item_id=med_id)
    patient = med.patient

    # You can't PATCH a medication over the API, so can't actually update the refills but we'll store it locally
    # update(user, 'medications', med_id, {'number_refills': new_refills})
    med.number_refills = max([med.number_refills - qty, 0])
    med.save()

    log_text = 'dispensed {0} x {1} to {2} {3}'.format(qty, med.name, patient.first_name, patient.last_name)
    AuditLog(user=user, text=log_text).save()

    # If the remaining refills drops below 2, send a reminder email
    if med.number_refills < 2:
        send_refill_email(patient, med)
        log_text = 'sent reminder email to {0} {1} at {2}'.format(patient.first_name, patient.last_name, patient.email)
        AuditLog(user=user, text=log_text).save()
