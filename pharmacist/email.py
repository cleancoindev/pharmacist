from django.core.mail import send_mail


def send_appt_email(patient, med):
    # TODO: move the email body to two templates, one HTML and one plain text

    if patient['email']:
        text = 'Your prescription for {0} is running low on refills. Please schedule an appointment with your care provider to renew the prescription.'
        text = text.format(med['name'])

        send_mail(
            'Time to Schedule a Doctor Visit',
            text,
            'no-reply@drchrono.com',
            [patient['email']],
            fail_silently=False,
        )

def send_refill_email(patient, med):
    if patient['email']:
        text = 'Your prescription for {0} is running low on refills. Please update it at: https://drchrono.com/patient_portal_link'
        text = text.format(med['name'])

        send_mail(
            'Time to Schedule a Doctor Visit',
            text,
            'no-reply@drchrono.com',
            [patient['email']],
            fail_silently=False,
        )
