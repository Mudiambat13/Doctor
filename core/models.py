from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

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
    
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
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
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Genre',
        blank=True
    )
    height = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name='Taille (cm)'
    )
    weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name='Poids (kg)'
    )
    allergies = models.TextField(
        blank=True, 
        verbose_name='Allergies'
    )
    medical_history = models.TextField(
        blank=True, 
        verbose_name='Antécédents médicaux'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Patient"

    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def bmi(self):
        if self.height and self.weight:
            height_in_meters = float(self.height) / 100
            return round(float(self.weight) / (height_in_meters ** 2), 2)
        return None

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
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
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
        return f"{self.reference} - {self.patient} avec {self.doctor} le {self.date}"

    class Meta:
        ordering = ['-date']

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('CANCELLED', 'Annulé')
    ]

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"RDV: {self.patient} avec Dr. {self.doctor} le {self.date}"
