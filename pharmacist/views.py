import json
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from drchrono_api import get_patients, get_meds


@login_required
def patient_list(request):
    context = RequestContext(request, {
        'patient_list': get_patients(request.user),
    })

    return render_to_response('patient_list.html', context)

@login_required
def dispense(request, patient_id):
    all_patients = get_patients(request.user)
    patient = filter(lambda p: p['id'] == int(patient_id), all_patients)
    med_list = get_meds(request.user, patient_id)

    # create a dict of meds indexed by id
    med_list_json = {}
    for m in med_list:
        med_list_json[m['id']] = m
    med_list_json = json.dumps(med_list_json)

    context = RequestContext(request, {
        'patient_id': patient_id,
        'med_list': med_list,
        'med_list_json': med_list_json,
    })

    return render_to_response('dispense.html', context)
