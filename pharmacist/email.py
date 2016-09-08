from django.core.mail import send_mail
from django.template.loader import render_to_string


def create_link_hash(patient):
    link_hash = 'sakjfdksklfds'
    return link_hash

def send_refill_email(patient, med):
    if patient.email:
        c = {
            'patient': patient,
            'med': med,
            'link_hash': create_link_hash(patient),
        }

        msg_html = render_to_string('email_refill.html', c)
        msg_plain = render_to_string('email_refill.txt', c)

        send_mail(
            'Time to Schedule a Doctor Visit',
            msg_plain,
            'no-reply@drchrono.com',
            [patient.email],
            fail_silently=False,
            html_message=msg_html,
        )
