from django.shortcuts import render_to_response
from django.views.generic import FormView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from drchrono_api import get_one, get_all, dispense_med
from forms import MedicationForm

@login_required
def patient_list(request):
    context = RequestContext(request, {
        'patient_list': get_all(request.user, 'patients'),
    })

    return render_to_response('patient_list.html', context)

@login_required
def dispense(request, patient_id):
    patient = get_one(request.user, 'patients', patient_id)
    med_list = get_all(request.user, 'medications', {'patient': patient_id}, patient=patient_id)
    name = '{0} {1}'.format(patient.first_name, patient.last_name)

    context = RequestContext(request, {
        'patient_id': patient_id,
        'med_list': med_list,
        'patient_name': name,
    })

    return render_to_response('dispense.html', context)

class ModifyView(FormView):
    template_name = 'modify.html'
    form_class = MedicationForm
    success_url = '#'

    def get_context_data(self, **kwargs):
        context = super(ModifyView, self).get_context_data(**kwargs)
        context['med_id'] = self.kwargs['med_id']
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        med_id = self.kwargs['med_id']
        qty = int(form.cleaned_data.get('quantity_to_dispense'))

        # Update the refill quantity available at Drchrono and send any needed emails
        dispense_med(self.request.user, form, med_id, qty)
        return super(ModifyView, self).form_valid(form)
