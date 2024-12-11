from django.contrib import admin
from .models import Appointment, Doctor ,Patient, Consultation

# Enregistrement des modèles
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Consultation)
