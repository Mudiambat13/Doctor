from django.contrib import admin
from django.utils.html import format_html
from .models import Patient, Doctor, Appointment, Consultation

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone_number', 'age', 'blood_group', 'get_bmi', 'created_at')
    list_filter = ('gender', 'blood_group', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': (('user', 'phone_number'), ('gender', 'date_of_birth'), 'address')
        }),
        ('Informations médicales', {
            'fields': (('blood_group', 'height', 'weight'), 'allergies', 'medical_history')
        }),
        ('Métadonnées', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nom complet'

    def get_bmi(self, obj):
        bmi = obj.bmi()
        if bmi:
            if bmi < 18.5:
                color = 'orange'
            elif 18.5 <= bmi < 25:
                color = 'green'
            else:
                color = 'red'
            return format_html('<span style="color: {};">{}</span>', color, bmi)
        return '-'
    get_bmi.short_description = 'IMC'

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('reference', 'patient', 'doctor', 'date', 'created_at')
    list_filter = ('doctor', 'date', 'created_at')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'reference')
    readonly_fields = ('reference', 'created_at', 'updated_at')

    fieldsets = (
        ('Informations générales', {
            'fields': ('reference', ('patient', 'doctor'), 'date')
        }),
        ('Détails médicaux', {
            'fields': ('symptoms', 'diagnosis', 'prescription', 'notes_medicales', 'recommandations')
        }),
        ('Suivi', {
            'fields': ('traitement', 'notes')
        }),
        ('Métadonnées', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'date', 'status', 'created_at')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'doctor__user__last_name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Rendez-vous', {
            'fields': (('patient', 'doctor'), 'date', 'status')
        }),
        ('Détails', {
            'fields': ('reason', 'notes')
        }),
        ('Métadonnées', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'

    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    get_doctor_name.short_description = 'Médecin'

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'speciality', 'phone', 'license_number', 'is_active')
    list_filter = ('speciality', 'is_active', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'license_number', 'phone')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('user', ('speciality', 'license_number'), 'phone')
        }),
        ('Informations professionnelles', {
            'fields': ('office_hours', 'is_active')
        }),
        ('Métadonnées', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_full_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"
    get_full_name.short_description = 'Nom complet'

# Personnalisation de l'interface d'administration
admin.site.site_header = 'Administration MediConnect'
admin.site.site_title = 'MediConnect'
admin.site.index_title = 'Tableau de bord administratif'
