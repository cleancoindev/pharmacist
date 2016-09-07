import requests, urllib


def get_all(user, endpoint, parameters={}):
    # TODO: wrap this in an error-handler / logger

    social = user.social_auth.get(user=user)
    access_token = social.extra_data['access_token']
    headers = {'Authorization': 'Bearer {0}'.format(access_token)}
    url = 'https://drchrono.com/api/{0}?{1}'.format(endpoint, urllib.urlencode(parameters))
    results = []

    while url:
        data = requests.get(url, headers=headers).json()
        results.extend(data['results'])
        url = data['next'] # A JSON null on the last page
    return results


def get_patients(user, summary=True):
    if summary:
        return get_all(user, 'patients_summary')
    return get_all(user, 'patients')

def get_doctors(user):
    return get_all(user, 'doctors')

def get_meds(user, patient_id):
    return get_all(user, 'medications', {'patient': patient_id})
