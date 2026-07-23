from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # ================= AUTH =================
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),

    # ================= DASHBOARD =================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html',
        success_url='/accounts/dashboard/'
    ), name='change_password'),

    # ================= ROLE PANELS =================
    path('doctor-panel/', views.doctor_panel, name='doctor_panel'),
    path('reception-panel/', views.reception_panel, name='reception_panel'),

    # ================= PATIENTS =================
    path('patients/', views.patients_list, name='patients_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/view/<uuid:pk>/', views.view_patient, name='view_patient'),
    path('patients/edit/<uuid:pk>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<uuid:pk>/', views.delete_patient, name='delete_patient'),

    # ================= DOCTORS =================
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/view/<uuid:pk>/', views.view_doctor, name='view_doctor'),
    path('doctors/edit/<uuid:pk>/', views.edit_doctor, name='edit_doctor'),
    path('doctors/delete/<uuid:pk>/', views.delete_doctor, name='delete_doctor'),

    # ================= APPOINTMENTS =================
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/view/<uuid:pk>/', views.view_appointment, name='view_appointment'),
    path('appointments/edit/<uuid:pk>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<uuid:pk>/', views.delete_appointment, name='delete_appointment'),

    # ================= MEDICINES =================
    path('medicines/', views.medicines_list, name='medicines_list'),
    path('medicines/add/', views.add_medicine, name='add_medicine'),
    path('medicines/view/<uuid:pk>/', views.view_medicine, name='view_medicine'),
    path('medicines/edit/<uuid:pk>/', views.edit_medicine, name='edit_medicine'),
    path('medicines/delete/<uuid:pk>/', views.delete_medicine, name='delete_medicine'),

    # ================= INVOICES =================
    path('invoices/', views.invoices_list, name='invoices_list'),
    path('invoices/add/', views.add_invoice, name='add_invoice'),
    path('invoices/view/<uuid:pk>/', views.view_invoice, name='view_invoice'),
    path('invoices/edit/<uuid:pk>/', views.edit_invoice, name='edit_invoice'),
    path('invoices/delete/<uuid:pk>/', views.delete_invoice, name='delete_invoice'),
    path('invoices/print/<uuid:pk>/', views.print_invoice, name='print_invoice'),

    # ================= REPORTS =================
    path('reports/', views.reports, name='reports'),

    # ================= 🌍 LANGUAGE SWITCHER =================
    path('change-language/<str:lang_code>/', views.change_language, name='change_language'),
]