from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    item_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    doctor = models.IntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    cell_phone = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    state = models.CharField(max_length=255, null=True)

    def save_from_dict(self, data):
        if not Patient.objects.filter(item_id=data.get('id')).exists():
            self.item_id = data.get('id')
            self.first_name = data.get('first_name')
            self.last_name = data.get('last_name')
            self.gender = data.get('gender')
            self.doctor = data.get('doctor')
            self.date_of_birth = data.get('date_of_birth')
            self.cell_phone = data.get('cell_phone')
            self.email = data.get('email')
            self.state = data.get('state')
            self.save()

class Medication(models.Model):
    item_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, null=True)
    patient = models.ForeignKey(Patient)
    doctor = models.IntegerField(null=True)
    pharmacy_note = models.CharField(max_length=1024, null=True)
    rxnorm = models.CharField(max_length=255, null=True)
    number_refills = models.IntegerField(null=True)

    def save_from_dict(self, data):
        if not Medication.objects.filter(item_id=data.get('id')).exists():
            self.item_id = data.get('id')
            self.name = data.get('name')
            self.patient = Patient.objects.get(item_id=data.get('patient'))
            self.doctor = data.get('doctor')
            self.pharmacy_note = data.get('pharmacy_note')
            self.rxnorm = data.get('rxnorm')
            self.number_refills = data.get('number_refills')
            self.save()

class AuditLog(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)

class EmailTracking(models.Model):
    SENT = 'sent'
    CLICKED = 'clicked'
    SCHEDULED = 'scheduled'

    STATE_CHOICES = (
        (SENT, 'email sent'),
        (CLICKED, 'link clicked'),
        (SCHEDULED, 'appointment scheduled'),
    )

    email_hash = models.CharField(max_length=255, unique=True, db_index=True)
    patient = models.ForeignKey(Patient)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
