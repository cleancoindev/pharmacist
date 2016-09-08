from django.shortcuts import render_to_response
from django.views.generic import FormView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from drchrono_api import DrchronoAPI, get_one, get_all, dispense_med
from models import Patient, Medication, AuditLog
from forms import MedicationForm

@login_required
def patient_list(request):
    DrchronoAPI(request.user).update()

    context = RequestContext(request, {
        'patient_list': Patient.objects.all(),
    })

    return render_to_response('patient_list.html', context)

@login_required
def dispense(request, patient_id):
    DrchronoAPI(request.user).update()

    patient = Patient.objects.get(item_id=patient_id)
    patient_name = '{0} {1}'.format(patient.first_name, patient.last_name)

    context = RequestContext(request, {
        'patient_id': patient_id,
        'med_list': Medication.objects.filter(patient=patient),
        'patient_name': patient_name,
    })

    return render_to_response('dispense.html', context)

@login_required
def audit_log(request):
    context = RequestContext(request, {
        'audit_log': AuditLog.objects.all(),
    })

    return render_to_response('audit_log.html', context)

class ModifyView(FormView):
    template_name = 'modify.html'
    form_class = MedicationForm
    success_url = '#'

    def get_context_data(self, **kwargs):
        context = super(ModifyView, self).get_context_data(**kwargs)
        context['med_id'] = self.kwargs['med_id']
        context['refills'] = xrange(1, int(self.kwargs['max_refills'])+1)
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        med_id = self.kwargs['med_id']
        qty = int(form.cleaned_data.get('quantity_to_dispense'))

        # Update the refill quantity available at Drchrono and send any needed emails
        dispense_med(self.request.user, form, med_id, qty)
        return super(ModifyView, self).form_valid(form)
