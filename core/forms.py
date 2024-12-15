from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Patient, Doctor, Appointment, Consultation
from django.utils import timezone

class UserRegistrationForm(UserCreationForm):
    """
    Formulaire d'inscription utilisateur étendant UserCreationForm.
    Ajoute les champs email, prénom et nom qui sont requis.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label='Prénom')
    last_name = forms.CharField(required=True, label='Nom')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class PatientRegistrationForm(forms.ModelForm):
    """
    Formulaire d'inscription pour les patients.
    Gère les informations spécifiques au patient comme le téléphone,
    l'adresse et la date de naissance.
    """
    class Meta:
        model = Patient
        fields = ['phone_number', 'address', 'date_of_birth', 'blood_group']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: +33 6 12 34 56 78'
            }),
            'address': forms.Textarea(attrs={'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'blood_group': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'phone_number': 'Téléphone',
            'address': 'Adresse',
            'date_of_birth': 'Date de naissance',
            'blood_group': 'Groupe sanguin'
        }

class AppointmentForm(forms.ModelForm):
    """
    Formulaire de création/modification de rendez-vous.
    Permet de sélectionner un médecin, une date/heure et 
    d'indiquer le motif de la consultation.
    """
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
                    'type': 'datetime-local',
                    'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'reason': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4,
                    'placeholder': 'Décrivez brièvement le motif de votre consultation'
                }
            )
        }
        labels = {
            'doctor': 'Médecin',
            'date': 'Date et heure du rendez-vous',
            'reason': 'Motif de la consultation'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer uniquement les médecins actifs
        self.fields['doctor'].queryset = Doctor.objects.filter(user__is_active=True)

class PatientSearchForm(forms.Form):
    """
    Formulaire de recherche pour les patients.
    Permet de rechercher des patients par nom ou email.
    """
    search = forms.CharField(
        required=False,
        label='Rechercher',
        widget=forms.TextInput(attrs={'placeholder': 'Nom ou email du patient'})
    )

class AppointmentFilterForm(forms.Form):
    """
    Formulaire de filtrage des rendez-vous.
    Permet de filtrer les rendez-vous par statut, période et médecin.
    """
    STATUS_CHOICES = [('', 'Tous')] + Appointment.STATUS_CHOICES
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label='Statut'
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Du'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Au'
    )

class DoctorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label='Prénom')
    last_name = forms.CharField(required=True, label='Nom')
    phone_number = forms.CharField(max_length=15, required=True, label='Téléphone')
    speciality = forms.CharField(max_length=100, required=True, label='Spécialité')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                speciality=self.cleaned_data['speciality'],
                phone_number=self.cleaned_data['phone_number']
            )
        return user

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone_number', 'address', 'date_of_birth', 'blood_group']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: +33 6 12 34 56 78'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Votre adresse complète'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'blood_group': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'phone_number': 'Numéro de téléphone',
            'address': 'Adresse',
            'date_of_birth': 'Date de naissance',
            'blood_group': 'Groupe sanguin'
        }
        help_texts = {
            'phone_number': 'Format international recommandé',
            'blood_group': 'Sélectionnez votre groupe sanguin si vous le connaissez'
        }

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['patient', 'doctor', 'date', 'diagnostic', 'traitement', 'notes', 'prescription']
        widgets = {
            'patient': forms.Select(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                }
            ),
            'doctor': forms.Select(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                }
            ),
            'date': forms.DateInput(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'type': 'date',
                }
            ),
            'diagnostic': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4,
                    'placeholder': 'Entrez le diagnostic'
                }
            ),
            'traitement': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4,
                    'placeholder': 'Décrivez le traitement prescrit'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4,
                    'placeholder': 'Notes additionnelles'
                }
            ),
            'prescription': forms.Textarea(
                attrs={
                    'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                    'rows': 4,
                    'placeholder': 'Détails de la prescription'
                }
            )
        }
        labels = {
            'patient': 'Patient',
            'doctor': 'Médecin',
            'date': 'Date de consultation',
            'diagnostic': 'Diagnostic',
            'traitement': 'Traitement',
            'notes': 'Notes',
            'prescription': 'Prescription'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si l'utilisateur est un médecin, pré-remplir et désactiver le champ doctor
        if user and hasattr(user, 'doctor'):
            self.fields['doctor'].initial = user.doctor
            self.fields['doctor'].disabled = True
            self.fields['doctor'].queryset = Doctor.objects.filter(id=user.doctor.id)
        else:
            self.fields['doctor'].queryset = Doctor.objects.filter(user__is_active=True)

        # Si l'utilisateur est un patient, pré-remplir et désactiver le champ patient
        if user and hasattr(user, 'patient'):
            self.fields['patient'].initial = user.patient
            self.fields['patient'].disabled = True
            self.fields['patient'].queryset = Patient.objects.filter(id=user.patient.id)
        else:
            self.fields['patient'].queryset = Patient.objects.all()

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Adresse email'
        }

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['speciality']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['address']
