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
    context = RequestContext(request, {
        'med_list': get_meds(request.user, patient_id),
    })

    return render_to_response('dispense.html', context)
