from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Patient(models.Model):
    """Modèle pour les patients qui peuvent s'inscrire via le site"""
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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Genre')
    blood_group = models.CharField(
        max_length=3, 
        choices=BLOOD_GROUPS, 
        blank=True,
        verbose_name='Groupe sanguin'
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
    allergies = models.TextField(blank=True, verbose_name='Allergies')
    medical_history = models.TextField(blank=True, verbose_name='Antécédents médicaux')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"

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
    """Modèle pour les médecins (géré uniquement via l'admin)"""
    SPECIALITY_CHOICES = [
        ('GENERAL', 'Médecine Générale'),
        ('CARDIO', 'Cardiologie'),
        ('DERMA', 'Dermatologie'),
        ('PEDIATRE', 'Pédiatrie'),
        ('OPHTALMO', 'Ophtalmologie'),
        ('GYNECO', 'Gynécologie'),
        ('ORTHO', 'Orthopédie'),
        ('NEURO', 'Neurologie'),
        ('PSYCHIATRE', 'Psychiatrie'),
        ('ORL', 'Oto-rhino-laryngologie'),
        ('GASTRO', 'Gastro-entérologie'),
        ('ENDOCRINO', 'Endocrinologie'),
        ('PNEUMO', 'Pneumologie'),
        ('NEPHRO', 'Néphrologie'),
        ('HEMATO', 'Hématologie'),
        ('RADIO', 'Radiologie'),
        ('URGENTISTE', 'Médecine d\'urgence'),
        ('CHIRURGIE', 'Chirurgie générale'),
        ('ANESTHESIE', 'Anesthésie-réanimation'),
        ('RHUMATO', 'Rhumatologie')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(
        max_length=50, 
        choices=SPECIALITY_CHOICES,
        verbose_name='Spécialité'
    )
    license_number = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name='Numéro de licence'
    )
    phone = models.CharField(max_length=15, verbose_name='Téléphone')
    office_hours = models.TextField(blank=True, verbose_name='Horaires de consultation')
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.get_speciality_display()}"

    class Meta:
        verbose_name = 'Médecin'
        verbose_name_plural = 'Médecins'
        ordering = ['user__last_name', 'user__first_name']

class Appointment(models.Model):
    """Modèle pour les rendez-vous"""
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmé'),
        ('CANCELLED', 'Annulé')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateTimeField(default=timezone.now)
    reason = models.TextField(verbose_name='Motif')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Statut'
    )
    notes = models.TextField(blank=True, verbose_name='Notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'

    def __str__(self):
        return f"RDV: {self.patient} avec Dr. {self.doctor} le {self.date}"

class Consultation(models.Model):
    """Modèle pour les consultations (créé après un rendez-vous)"""
    reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Docteur')
    date = models.DateField(default=timezone.now, verbose_name='Date de consultation')
    symptoms = models.TextField(verbose_name="Symptômes", blank=True, default="")
    diagnosis = models.TextField(blank=True, verbose_name='Diagnostic')
    traitement = models.TextField(blank=True, verbose_name='Traitement')
    notes = models.TextField(blank=True, verbose_name='Notes de consultation')
    prescription = models.TextField(blank=True, verbose_name='Prescription')
    notes_medicales = models.TextField(verbose_name="Notes médicales", blank=True)
    recommandations = models.TextField(verbose_name="Recommandations", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.patient} avec {self.doctor} le {self.date}"

    class Meta:
        ordering = ['-date']
