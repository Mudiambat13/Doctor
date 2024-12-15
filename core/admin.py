from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment, Consultation

class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Informations du médecin'

class CustomUserAdmin(UserAdmin):
    inlines = (DoctorInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_doctor')
    
    def is_doctor(self, obj):
        return hasattr(obj, 'doctor')
    is_doctor.boolean = True
    is_doctor.short_description = 'Médecin'

# Ré-enregistrer UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'speciality', 'license_number', 'phone', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'speciality')
    list_filter = ('speciality', 'is_active')

# Enregistrement des modèles
admin.site.register(Appointment)
admin.site.register(Patient)
admin.site.register(Consultation)
