from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Patient, Appointment, Consultation, Doctor
from django.utils import timezone

class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription pour les patients"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label='Prénom')
    last_name = forms.CharField(required=True, label='Nom')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Créer automatiquement un profil patient
            Patient.objects.create(user=user)
        return user

class PatientProfileForm(forms.ModelForm):
    """Formulaire de profil patient"""
    class Meta:
        model = Patient
        fields = ['phone_number', 'address', 'date_of_birth', 'blood_group', 'height', 'weight', 'allergies', 'medical_history']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
        }

class AppointmentForm(forms.ModelForm):
    """Formulaire de rendez-vous"""
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'reason']
        widgets = {
            'doctor': forms.Select(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                }
            ),
            'date': forms.DateTimeInput(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'type': 'datetime-local'
                }
            ),
            'reason': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4,
                    'placeholder': 'Raison du rendez-vous'
                }
            )
        }
        labels = {
            'doctor': 'Médecin',
            'date': 'Date et heure',
            'reason': 'Motif du rendez-vous'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(user__is_active=True)

class ConsultationForm(forms.ModelForm):
    """Formulaire de consultation (réservé aux médecins)"""
    class Meta:
        model = Consultation
        fields = ['patient', 'doctor', 'date', 'diagnosis', 'traitement', 'notes', 'prescription']
        widgets = {
            'patient': forms.Select(
                attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}
            ),
            'doctor': forms.Select(
                attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}
            ),
            'date': forms.DateInput(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'type': 'date'
                }
            ),
            'diagnosis': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4
                }
            ),
            'traitement': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4
                }
            ),
            'prescription': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4
                }
            )
        }

class UserUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour des informations utilisateur"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }

class CustomLoginForm(AuthenticationForm):
    """Formulaire de connexion personnalisé"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nom d\'utilisateur'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Mot de passe'
    }))

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['speciality', 'license_number', 'phone']
        widgets = {
            'speciality': forms.TextInput(
                attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}
            ),
            'license_number': forms.TextInput(
                attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}
            )
        }
        labels = {
            'speciality': 'Spécialité',
            'license_number': 'Numéro de licence',
            'phone': 'Téléphone'
        }
