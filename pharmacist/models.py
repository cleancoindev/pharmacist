from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Patient(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True,)
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='patients')
    date_of_birth = models.DateField(null=True)
    doctor = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    cell_phone = models.CharField(max_length=255)
    email = models.EmailField()
    state = models.CharField(max_length=255)

class Doctor(models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True,)
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='doctors')
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

