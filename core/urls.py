from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Authentification et profil
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='core/auth/login.html'), name='login'),
    
    # Tableau de bord
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    
    # Gestion des médecins
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    
    # Gestion des patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    
    # Gestion des rendez-vous
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
    path('appointments/<int:pk>/confirm/', views.appointment_confirm, name='appointment_confirm'),
] 