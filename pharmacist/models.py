from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    doctor_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    suffix = models.CharField(max_length=255, null=True)
    job_title = models.CharField(max_length=255, null=True)
    specialty = models.CharField(max_length=255)
    cell_phone = models.CharField(max_length=255, null=True)
    home_phone = models.CharField(max_length=255, null=True)
    office_phone = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    website = models.CharField(max_length=255, null=True)

class Patient(models.Model):
    patient_id = models.IntegerField(unique=True)
    doctor = models.ForeignKey(Doctor)
    date_of_birth = models.DateField(null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    cell_phone = models.CharField(max_length=255)
    email = models.EmailField()
    state = models.CharField(max_length=255)

class Medication(models.Model):
    med_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Doctor)
    pharmacy_note = models.CharField(max_length=1024)
    rxnorm = models.CharField(max_length=255)
    number_refills = models.IntegerField()
