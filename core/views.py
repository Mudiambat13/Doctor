from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment, Doctor, Patient, Consultation
from .forms import AppointmentForm, UserRegistrationForm, PatientProfileForm,ConsultationForm, UserUpdateForm, DoctorProfileForm
from django.contrib.auth.forms import UserChangeForm
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def home(request):
    return render(request, 'core/home.html', {
        'title': 'Accueil'
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/auth/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'core/auth/login.html'
    
    def get_success_url(self):
        print(f"get_success_url appelé pour: {self.request.user}")
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        
        if hasattr(self.request.user, 'doctor'):
            return reverse_lazy('core:doctor_dashboard')
        elif hasattr(self.request.user, 'patient'):
            return reverse_lazy('core:patient_dashboard')
        else:
            messages.warning(self.request, "Type d'utilisateur non reconnu.")
            return reverse_lazy('core:home')

@login_required
def dashboard_redirect(request):
    """Vue de redirection générale du tableau de bord"""
    print(f"User: {request.user}")  # Debug
    print(f"Is authenticated: {request.user.is_authenticated}")  # Debug
    print(f"Has doctor: {hasattr(request.user, 'doctor')}")  # Debug
    print(f"Has patient: {hasattr(request.user, 'patient')}")  # Debug

    if not request.user.is_authenticated:
        messages.error(request, "Veuillez vous connecter d'abord.")
        return redirect('login')

    if hasattr(request.user, 'doctor'):
        return redirect('core:doctor_dashboard')
    elif hasattr(request.user, 'patient'):
        return redirect('core:patient_dashboard')
    else:
        messages.warning(request, "Type d'utilisateur non reconnu.")
        return redirect('core:home')

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, "Accès non autorisé. Vous n'êtes pas un médecin.")
        return redirect('core:home')
    
    # Récupérer les rendez-vous récents
    recent_appointments = Appointment.objects.filter(
        doctor=request.user.doctor
    ).order_by('-date', '-time')[:5]  # 5 derniers rendez-vous

    # Récupérer les consultations récentes
    recent_consultations = Consultation.objects.filter(
        doctor=request.user.doctor
    ).order_by('-date')[:5]  # 5 dernières consultations

    # Compter le nombre total de patients uniques
    patients_count = Patient.objects.filter(
        appointment__doctor=request.user.doctor
    ).distinct().count()

    context = {
        'user': request.user,
        'doctor': request.user.doctor,
        'recent_appointments': recent_appointments,
        'recent_consultations': recent_consultations,
        'appointments': Appointment.objects.filter(doctor=request.user.doctor),
        'consultations': Consultation.objects.filter(doctor=request.user.doctor),
        'patients_count': patients_count,
    }
    return render(request, 'core/doctors/dashboard.html', context)

@login_required
def patient_dashboard(request):
    if not hasattr(request.user, 'patient'):
        messages.error(request, "Accès non autorisé. Vous n'êtes pas un patient.")
        return redirect('core:home')
    
    context = {
        'user': request.user,
        'patient': request.user.patient,
        # Ajoutez d'autres données nécessaires
    }
    return render(request, 'core/patients/dashboard.html', context)

@login_required
def appointment_list(request):
    # Logique pour récupérer et afficher les rendez-vous
    return render(request, 'core/appointments/appointment_list.html', {})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.save()
            messages.success(request, 'Votre rendez-vous a été créé avec succès!')
            return redirect('core:appointment_list')
    else:
        form = AppointmentForm()
    
    return render(request, 'core/appointments/appointment_form.html', {
        'form': form,
        'title': 'Nouveau rendez-vous'
    })

@login_required
def appointment_detail(request, pk):
    # Logique d'affichage des détails du rendez-vous
    return render(request, 'core/appointments/appointment_detail.html')

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
    return render(request, 'core/appointments/appointment_form.html', context)

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
    return render(request, 'core/patients/patient_list.html', {
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

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        if hasattr(request.user, 'doctor'):
            profile_form = DoctorProfileForm(request.POST, instance=request.user.doctor)
        elif hasattr(request.user, 'patient'):
            profile_form = PatientProfileForm(request.POST, instance=request.user.patient)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('core:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        if hasattr(request.user, 'doctor'):
            profile_form = DoctorProfileForm(instance=request.user.doctor)
        elif hasattr(request.user, 'patient'):
            profile_form = PatientProfileForm(instance=request.user.patient)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'core/profile.html', context)

@login_required
def doctor_list(request):
    """Vue pour afficher la liste des médecins"""
    doctors = Doctor.objects.all()
    return render(request, 'core/doctors/doctor_list.html', {
        'doctors': doctors,
        'title': 'Nos médecins'
    })

@login_required
def doctor_detail(request, pk):
    """Vue pour afficher le détail d'un médecin"""
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = Appointment.objects.filter(doctor=doctor)
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'title': f'Dr. {doctor.user.get_full_name()}'
    }
    return render(request, 'core/doctors/doctor_detail.html', context)

@login_required
def appointment_confirm(request, pk):
    """Vue pour confirmer un rendez-vous (réservée aux médecins)"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Vérifier que l'utilisateur est le médecin concerné
    if not hasattr(request.user, 'doctor') or request.user.doctor != appointment.doctor:
        messages.error(request, "Vous n'avez pas le droit de confirmer ce rendez-vous.")
        return redirect('core:appointment_list')
    
    # Vérifier que le rendez-vous est en attente
    if appointment.status != 'PENDING':
        messages.error(request, "Ce rendez-vous ne peut pas être confirmé.")
        return redirect('core:appointment_detail', pk=appointment.pk)
    
    if request.method == 'POST':
        appointment.status = 'CONFIRMED'
        appointment.save()
        messages.success(request, 'Le rendez-vous a été confirmé avec succès!')
        
        # Vous pouvez ajouter ici l'envoi d'un email de confirmation au patient
        
        return redirect('core:appointment_detail', pk=appointment.pk)
    
    return render(request, 'core/appointments/appointment_confirm.html', {
        'appointment': appointment,
        'title': 'Confirmer le rendez-vous'
    })

@login_required
def consultation_create(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST, user=request.user)
        if form.is_valid():
            consultation = form.save(commit=False)
            if hasattr(request.user, 'patient'):
                consultation.patient = request.user.patient
            if hasattr(request.user, 'doctor'):
                consultation.doctor = request.user.doctor
            consultation.save()
            messages.success(request, 'La consultation a été créée avec succès.')
            return redirect('core:consultation_list')
    else:
        form = ConsultationForm(user=request.user)
    
    return render(request, 'core/consultations/consultation_form.html', {
        'form': form,
        'title': 'Nouvelle Consultation'
    })

@login_required
def consultation_detail(request, pk):
    consultation = get_object_or_404(Consultation, pk=pk)
    
    # Vérification des permissions
    if hasattr(request.user, 'patient') and request.user.patient == consultation.patient:
        authorized = True
    elif hasattr(request.user, 'doctor') and request.user.doctor == consultation.doctor:
        authorized = True
    else:
        authorized = False

    if not authorized:
        messages.error(request, "Vous n'avez pas accès à cette consultation.")
        return redirect('core:home')

    return render(request, 'core/consultations/consultation_detail.html', {
        'consultation': consultation
    })

@login_required
def consultation_list(request):
    if hasattr(request.user, 'patient'):
        consultations = Consultation.objects.filter(patient=request.user.patient)
    elif hasattr(request.user, 'doctor'):
        consultations = Consultation.objects.filter(doctor=request.user.doctor)
    else:
        messages.error(request, "Accès non autorisé.")
        return redirect('core:home')
    
    return render(request, 'core/consultations/consultation_list.html', {
        'consultations': consultations
    })

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Vérifier que l'utilisateur a le droit de modifier ce rendez-vous
    if not (request.user.is_staff or appointment.patient.user == request.user):
        messages.error(request, "Vous n'avez pas la permission de modifier ce rendez-vous.")
        return redirect('core:appointment_list')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le rendez-vous a été modifié avec succès.')
            return redirect('core:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'core/appointments/appointment_form.html', {
        'form': form,
        'appointment': appointment,
        'title': 'Modifier le rendez-vous'
    })

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Vérifier que l'utilisateur a le droit de supprimer ce rendez-vous
    if not (request.user.is_staff or appointment.patient.user == request.user):
        messages.error(request, "Vous n'avez pas la permission de supprimer ce rendez-vous.")
        return redirect('core:appointment_list')

    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Le rendez-vous a été supprimé avec succès.')
        return redirect('core:appointment_list')

    return render(request, 'core/appointments/appointment_confirm_delete.html', {
        'appointment': appointment
    })
