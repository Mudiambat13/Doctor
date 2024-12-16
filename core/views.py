from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient, Doctor, Appointment, Consultation
from .forms import AppointmentForm, ConsultationForm, PatientProfileForm, UserUpdateForm

@login_required
def dashboard(request):
    if hasattr(request.user, 'patient'):
        return redirect('core:patient_dashboard')
    elif hasattr(request.user, 'doctor'):
        return redirect('core:doctor_dashboard')
    return redirect('login')

@login_required
def patient_dashboard(request):
    if not hasattr(request.user, 'patient'):
        return redirect('core:profile')
    
    context = {
        'patient': request.user.patient,
        'title': 'Tableau de bord Patient'
    }
    return render(request, 'core/patient/dashboard.html', context)

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('core:dashboard')
    
    appointments = Appointment.objects.filter(doctor=request.user.doctor)
    consultations = Consultation.objects.filter(doctor=request.user.doctor)
    
    context = {
        'appointments': appointments,
        'consultations': consultations,
    }
    return render(request, 'core/doctors/dashboard.html', context)

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            messages.success(request, 'Rendez-vous créé avec succès!')
            return redirect('core:patient_dashboard')
    else:
        form = AppointmentForm()
    
    return render(request, 'core/appointments/appointment_form.html', {'form': form})

@login_required
def consultation_create(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save()
            messages.success(request, 'Consultation créée avec succès!')
            return redirect('core:doctor_dashboard')
    else:
        form = ConsultationForm()
    
    return render(request, 'core/consultations/create.html', {'form': form})

@login_required
def profile(request):
    # Récupérer ou créer le profil patient si nécessaire
    patient, created = Patient.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Traitement du formulaire soumis
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = PatientProfileForm(request.POST, instance=patient)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('core:profile')
        else:
            messages.error(request, 'Erreur lors de la mise à jour du profil. Veuillez corriger les erreurs.')
    else:
        # Affichage initial du formulaire
        user_form = UserUpdateForm(instance=request.user)
        profile_form = PatientProfileForm(instance=patient)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Mon Profil',
        'patient': patient
    }
    
    return render(request, 'core/profile.html', context)

def home(request):
    """Vue de la page d'accueil accessible sans authentification"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/home.html', {
        'title': 'Accueil - MediConnect'
    })

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'core/doctors/doctor_list.html', {
        'doctors': doctors
    })

@login_required
def appointment_list(request):
    if hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(patient=request.user.patient)
    elif hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
    else:
        appointments = []
    
    return render(request, 'core/appointments/appointment_list.html', {
        'appointments': appointments
    })

@login_required
def consultation_list(request):
    if hasattr(request.user, 'doctor'):
        consultations = Consultation.objects.filter(doctor=request.user.doctor)
    elif hasattr(request.user, 'patient'):
        consultations = Consultation.objects.filter(patient=request.user.patient)
    else:
        consultations = []
    
    return render(request, 'core/consultations/consultation_list.html', {
        'consultations': consultations
    })

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # L'utilisateur est déjà lié au patient grâce à la méthode save() du formulaire
            login(request, user)
            messages.success(request, "Inscription réussie! Bienvenue sur MediConnect.")
            return redirect('core:patient_dashboard')
        else:
            messages.error(request, "Erreur lors de l'inscription. Veuillez corriger les erreurs ci-dessous.")
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'registration/register_patient.html', {
        'form': form,
        'title': 'Inscription Patient'
    })
