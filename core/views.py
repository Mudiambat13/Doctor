from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient, Doctor, Appointment, Consultation
from .forms import AppointmentForm, ConsultationForm, PatientProfileForm

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
        return redirect('core:dashboard')
    
    appointments = Appointment.objects.filter(patient=request.user.patient)
    consultations = Consultation.objects.filter(patient=request.user.patient)
    
    context = {
        'appointments': appointments,
        'consultations': consultations,
    }
    return render(request, 'core/patients/dashboard.html', context)

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
    
    return render(request, 'core/appointments/create.html', {'form': form})

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
    try:
        if hasattr(request.user, 'patient'):
            return render(request, 'core/profile.html', {'profile': request.user.patient})
        else:
            return render(request, 'core/error.html', {
                'error_title': 'Profil non trouvé',
                'error_message': 'Vous n\'avez pas encore de profil patient.',
                'back_url': 'core:home'
            })
    except Exception as e:
        return render(request, 'core/error.html', {
            'error_title': 'Erreur',
            'error_message': 'Une erreur est survenue lors de l\'accès à votre profil.',
            'back_url': 'core:home'
        })

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
