from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('^', include('django.contrib.auth.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'patient_list/', views.patient_list, name='patient_list'),
    url(r'dispense/(?P<patient_id>[0-9]+)/', views.dispense, name='dispense'),
    url(r'schedule/(?P<patient_id>[0-9]+)/', views.schedule, name='schedule'),
    url(r'modify/(?P<med_id>[0-9]+)/(?P<max_refills>[0-9]+)/', views.ModifyView.as_view(), name='modify'),
    url(r'patient_auth/(?P<email_hash>\w{16})/', views.PatientAuthView.as_view(), name='patient_auth'),
    url(r'audit_log/', views.audit_log, name='audit_log'),
]
