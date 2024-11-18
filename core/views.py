from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment, Doctor, Patient
from .forms import AppointmentForm, UserRegistrationForm, PatientProfileForm
from django.contrib.auth.forms import UserChangeForm

def home(request):
    return render(request, 'core/home.html', {
        'title': 'Accueil'
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer un profil patient pour l'utilisateur
            Patient.objects.create(user=user)
            messages.success(request, 'Votre compte a été créé avec succès! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/auth/register.html', {'form': form})

@login_required
def dashboard(request):
    context = {
        'title': 'Tableau de bord'
    }
    
    if hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
        return render(request, 'core/doctor_dashboard.html', {
            **context,
            'appointments': appointments
        })
    else:
        appointments = Appointment.objects.filter(patient=request.user.patient)
        return render(request, 'core/patient_dashboard.html', {
            **context,
            'appointments': appointments
        })

@login_required
def appointment_list(request):
    if hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
    else:
        appointments = Appointment.objects.filter(patient=request.user.patient)
    
    context = {
        'appointments': appointments,
        'title': 'Mes rendez-vous'
    }
    return render(request, 'core/appointment_list.html', context)

@login_required
def appointment_create(request):
    if hasattr(request.user, 'doctor'):
        messages.error(request, 'Seuls les patients peuvent prendre rendez-vous.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.status = 'PENDING'
            appointment.save()
            messages.success(request, 'Votre rendez-vous a été créé avec succès!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    
    context = {
        'form': form,
        'title': 'Nouveau rendez-vous',
        'doctors': Doctor.objects.all()
    }
    return render(request, 'core/appointment_form.html', context)

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Vérifier que l'utilisateur a le droit de voir ce rendez-vous
    if not (hasattr(request.user, 'doctor') and request.user.doctor == appointment.doctor) and \
       not (hasattr(request.user, 'patient') and request.user.patient == appointment.patient):
        messages.error(request, "Vous n'avez pas accès à ce rendez-vous.")
        return redirect('dashboard')
    
    return render(request, 'core/appointment_detail.html', {
        'appointment': appointment,
        'title': f'Rendez-vous du {appointment.date}'
    })

@login_required
def appointment_edit(request, pk):
    """Vue pour modifier un rendez-vous"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Vérifier que l'utilisateur a le droit de modifier ce rendez-vous
    if not (hasattr(request.user, 'patient') and request.user.patient == appointment.patient):
        messages.error(request, "Vous n'avez pas le droit de modifier ce rendez-vous.")
        return redirect('appointment_list')
    
    # Vérifier que le rendez-vous est encore modifiable (status PENDING)
    if appointment.status != 'PENDING':
        messages.error(request, "Ce rendez-vous ne peut plus être modifié.")
        return redirect('appointment_detail', pk=appointment.pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le rendez-vous a été modifié avec succès!')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    
    context = {
        'form': form,
        'title': 'Modifier le rendez-vous',
        'appointment': appointment,
        'is_edit': True
    }
    return render(request, 'core/appointment_form.html', context)

@login_required
def appointment_cancel(request, pk):
    """Vue pour annuler un rendez-vous"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Vérifier les droits d'accès
    if not (hasattr(request.user, 'patient') and request.user.patient == appointment.patient) and \
       not (hasattr(request.user, 'doctor') and request.user.doctor == appointment.doctor):
        messages.error(request, "Vous n'avez pas le droit d'annuler ce rendez-vous.")
        return redirect('appointment_list')
    
    # Vérifier que le rendez-vous peut être annulé
    if appointment.status not in ['PENDING', 'CONFIRMED']:
        messages.error(request, "Ce rendez-vous ne peut plus être annulé.")
        return redirect('appointment_detail', pk=appointment.pk)
    
    if request.method == 'POST':
        appointment.status = 'CANCELLED'
        appointment.save()
        messages.success(request, 'Le rendez-vous a été annulé.')
        return redirect('appointment_list')
    
    return render(request, 'core/appointment/appointment_cancel.html', {
        'appointment': appointment,
        'title': 'Annuler le rendez-vous'
    })

@login_required
def patient_list(request):
    """Vue pour afficher la liste des patients (réservée aux médecins)"""
    if not hasattr(request.user, 'doctor'):
        messages.error(request, "Accès réservé aux médecins.")
        return redirect('dashboard')
    
    patients = Patient.objects.all()
    return render(request, 'core/patient_list.html', {
        'patients': patients,
        'title': 'Liste des patients'
    })

@login_required
def patient_detail(request, pk):
    """Vue pour afficher le détail d'un patient"""
    patient = get_object_or_404(Patient, pk=pk)
    
    # Vérifier les droits d'accès
    if not hasattr(request.user, 'doctor') and request.user.patient != patient:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('dashboard')
    
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'core/patient_detail.html', {
        'patient': patient,
        'appointments': appointments,
        'title': f'Patient : {patient.user.get_full_name()}'
    })

@login_required
def patient_edit(request, pk):
    """Vue pour modifier le profil d'un patient"""
    patient = get_object_or_404(Patient, pk=pk)
    
    # Vérifier les droits d'accès
    if not hasattr(request.user, 'doctor') and request.user.patient != patient:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=patient.user)
        profile_form = PatientProfileForm(request.POST, instance=patient)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        user_form = UserChangeForm(instance=patient.user)
        profile_form = PatientProfileForm(instance=patient)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'patient': patient,
        'title': 'Modifier le profil'
    }
    return render(request, 'core/patient_edit.html', context)
