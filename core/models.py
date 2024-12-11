from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Patient(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Numéro de téléphone')
    address = models.TextField(blank=True, verbose_name='Adresse')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date de naissance')
    blood_group = models.CharField(
        max_length=3, 
        choices=BLOOD_GROUPS, 
        blank=True,
        verbose_name='Groupe sanguin'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Patient"

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Docteur')
    date = models.DateField(default=timezone.now, verbose_name='Date de consultation')
    diagnostic = models.TextField(blank=True, verbose_name='Diagnostic')
    traitement = models.TextField(blank=True, verbose_name='Traitement')
    notes = models.TextField(blank=True, verbose_name='Notes de consultation')
    prescription = models.TextField(blank=True, verbose_name='Prescription')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation de {self.patient} avec {self.doctor} le {self.date}"

    class Meta:
        ordering = ['-date']

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('CANCELLED', 'Annulé'),
        ('COMPLETED', 'Terminé'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(default=timezone.now)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"RDV: {self.patient} avec {self.doctor} le {self.date} à {self.time}"
