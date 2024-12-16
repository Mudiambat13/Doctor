from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/patient/', views.register_patient, name='register_patient'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('consultations/', views.consultation_list, name='consultation_list'),
    path('appointment/create/', views.appointment_create, name='appointment_create'),
    path('consultation/create/', views.consultation_create, name='consultation_create'),
    path('profile/', views.profile, name='profile'),
] 