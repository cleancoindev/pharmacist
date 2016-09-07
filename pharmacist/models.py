from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    item_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    website = models.CharField(max_length=255, null=True)

    def save_from_dict(self, data):
        self.item_id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.website = data.get('website')
        self.save()

class Patient(models.Model):
    item_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    doctor = models.ForeignKey(Doctor)
    date_of_birth = models.DateField(null=True)
    cell_phone = models.CharField(max_length=255)
    email = models.EmailField()
    state = models.CharField(max_length=255)

    def save_from_dict(self, data):
        self.item_id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.doctor = Doctor.objects.get(item_id=data.get('doctor'))
        self.date_of_birth = data.get('date_of_birth')
        self.cell_phone = data.get('cell_phone')
        self.email = data.get('email')
        self.state = data.get('state')
        self.save()

class Medication(models.Model):
    item_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Doctor)
    pharmacy_note = models.CharField(max_length=1024)
    rxnorm = models.CharField(max_length=255)
    number_refills = models.IntegerField()

    def save_from_dict(self, data):
        self.item_id = data.get('id')
        self.name = data.get('name')
        self.patient = Patient.objects.get(item_id=data.get('patient'))
        self.doctor = Doctor.objects.get(item_id=data.get('doctor'))
        self.pharmacy_note = data.get('pharmacy_note')
        self.rxnorm = data.get('rxnorm')
        self.number_refills = data.get('number_refills')
        self.save()
