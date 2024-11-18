from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Patient, Doctor, Appointment

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
        fields = ['phone', 'address', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'phone': 'Téléphone',
            'address': 'Adresse',
            'date_of_birth': 'Date de naissance',
        }

class AppointmentForm(forms.ModelForm):
    """
    Formulaire de création/modification de rendez-vous.
    Permet de sélectionner un médecin, une date/heure et 
    d'indiquer le motif de la consultation.
    """
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ne montre que les médecins actifs
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
