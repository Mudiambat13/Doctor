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
        labels = {
            'phone_number': 'Numéro de téléphone',
            'address': 'Adresse',
            'date_of_birth': 'Date de naissance',
            'blood_group': 'Groupe sanguin',
            'height': 'Taille (cm)',
            'weight': 'Poids (kg)',
            'allergies': 'Allergies',
            'medical_history': 'Antécédents médicaux'
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input rounded-md'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-textarea rounded-md'
            }),
            'allergies': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-textarea rounded-md'
            }),
            'medical_history': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-textarea rounded-md'
            }),
            'phone_number': forms.TextInput(attrs={'class': 'form-input rounded-md'}),
            'height': forms.NumberInput(attrs={'class': 'form-input rounded-md'}),
            'weight': forms.NumberInput(attrs={'class': 'form-input rounded-md'}),
            'blood_group': forms.Select(attrs={'class': 'form-select rounded-md'})
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
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Adresse email',
            'first_name': 'Prénom',
            'last_name': 'Nom'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input rounded-md'}),
            'email': forms.EmailInput(attrs={'class': 'form-input rounded-md'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input rounded-md'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input rounded-md'})
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

class PatientRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'exemple@email.com'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Adresse email',
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe'
        }
        help_texts = {
            'username': 'Lettres, chiffres et @/./+/-/_ uniquement.',
            'password1': 'Votre mot de passe doit contenir au moins 8 caractères.',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Votre nom d\'utilisateur'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Votre mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Confirmez votre mot de passe'
        })
        
        # Personnalisation des labels
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmation du mot de passe'
        
        # Personnalisation des messages d'aide
        self.fields['password1'].help_text = 'Le mot de passe doit contenir au moins 8 caractères et ne peut pas être entièrement numérique.'
        self.fields['password2'].help_text = 'Entrez le même mot de passe que précédemment, pour vérification.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            Patient.objects.create(user=user)
            
        return user
