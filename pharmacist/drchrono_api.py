import requests, urllib
from django.forms import model_to_dict
from email import send_appt_email, send_refill_email
from models import Patient, Medication


endpoint_models = {
    'patients': Patient,
    'medications': Medication,
    }


def get_one(user, endpoint, item_id, parameters={}):
    # First, try to retrieve data from our DB if we've retrieved it from the API previously
    model = endpoint_models[endpoint]
    try:
        data = model_to_dict(model.objects.get(item_id=item_id))
    except:
        # Get it from the API directly
        # TODO: wrap this in an error-handler / logger
        social = user.social_auth.get(user=user)
        access_token = social.extra_data['access_token']
        headers = {'Authorization': 'Bearer {0}'.format(access_token)}
        url = 'https://drchrono.com/api/{0}/{1}?{2}'.format(endpoint, item_id, urllib.urlencode(parameters))
        data = requests.get(url, headers=headers).json()

        # Save the item in the DB for future reference
        print data
        model().save_from_dict(data)
    return data

def get_all(user, endpoint, parameters={}):
    # Try the DB first for data
    model = endpoint_models[endpoint]
    results = model.objects.values()

    if not len(results):
        # Get it from the API directly
        # TODO: wrap this in an error-handler / logger
        social = user.social_auth.get(user=user)
        access_token = social.extra_data['access_token']
        headers = {'Authorization': 'Bearer {0}'.format(access_token)}
        url = 'https://drchrono.com/api/{0}?{1}'.format(endpoint, urllib.urlencode(parameters))
        results = []

        # Fetch the objects one "page" at a time
        while url:
            data = requests.get(url, headers=headers).json()
            results.extend(data['results'])
            url = data['next'] # A JSON null on the last page

    # Persist the results as individual items in the DB
    for item in results:
        model().save_from_dict(item)
    return results

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
    med = get_one(user, 'medications', med_id)
    patient = get_one(user, 'patients', med['patient'])
    new_refills = med['number_refills'] - qty
    text = str(new_refills) + ' refills remain'

    # You can't PATCH a medication over the API, so can't actually update the refills -- name a note instead
    # update(user, 'medications', med_id, {'number_refills': new_refills})
    update(user, 'medications/{0}/append_to_pharmacy_note'.format(med_id), None, {'text': text})

    # If the remaining refills drops below 2, send a reminder email
    if new_refills < 2:
        # If there's a pharmacy note containing "appt", then send an appointment email
        if 'appt' in med['pharmacy_note'].lower():
            send_appt_email(patient, med)
        else:
            # Regular refill reminder without an appointment needed
            send_refill_email(patient, med)

