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
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='core:home',
        http_method_names=['get', 'post']
    ), name='logout'),
    
    # Tableau de bord
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
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
    path('appointment/create/', views.appointment_create, name='appointment_create'),
    path('appointment/<int:pk>/update/', views.appointment_update, name='appointment_update'),
    path('appointment/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
    path('appointments/<int:pk>/confirm/', views.appointment_confirm, name='appointment_confirm'),
    path('consultation/create/', views.consultation_create, name='consultation_form'),
    path('appointment/create/', views.appointment_create, name='appointment_create'),
    path('appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('consultations/', views.consultation_list, name='consultation_list'),
    path('consultations/create/', views.consultation_create, name='consultation_form'),
    path('consultations/<int:pk>/', views.consultation_detail, name='consultation_detail'),
] 