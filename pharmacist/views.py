from django.shortcuts import render_to_response
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.exceptions import ValidationError
from drchrono_api import DrchronoAPI, dispense_med
from models import Patient, Medication, AuditLog, EmailTracking
from forms import MedicationForm, PatientAuthForm

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
        'patient_name': patient_name,
        'med_list': Medication.objects.filter(patient=patient),
    })

    return render_to_response('dispense.html', context)

def schedule(request, patient_id):
    patient = Patient.objects.get(item_id=patient_id)
    context = RequestContext(request, {
        'patient': patient,
    })

    return render_to_response('schedule.html', context)

@login_required
def audit_log(request):
    context = RequestContext(request, {
        'audit_log': AuditLog.objects.all(),
    })

    return render_to_response('audit_log.html', context)

class PatientAuthView(FormView):
    template_name = 'patient_auth.html'
    form_class = PatientAuthForm

    def _get_email(self):
        email_hash = self.kwargs['email_hash']
        return get_object_or_404(EmailTracking, email_hash=email_hash)

    def get_success_url(self):
        return '/schedule/{0}/'.format(self.patient.item_id)

    def get_context_data(self, **kwargs):
        context = super(PatientAuthView, self).get_context_data(**kwargs)
        email = self._get_email()
        email.state = EmailTracking.CLICKED
        email.save()

        log_text = 'email appointment scheduling link clicked by {0} {1}'.format(email.patient.first_name, email.patient.first_name)
        AuditLog(user=None, text=log_text).save()

        context['patient'] = email.patient
        return context

    def form_valid(self, form):
        email = self._get_email()
        ssn = form.cleaned_data.get('ssn')
        self.patient = email.patient
        
        if ssn != email.patient.ssn:
            form.add_error('ssn', 'SSN does not match our records!')
            return super(PatientAuthView, self).form_invalid(form)

        return super(PatientAuthView, self).form_valid(form)

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
