from django.contrib import admin
# شيلنا الـ User من السطر اللي جاي ده
from .models import (Department, Doctor, Patient, Appointment, 
                     MedicalRecord, Medicine, Prescription, PrescriptionItem, 
                     Payment, Invoice, ClinicSettings)


# مسحنا البلوك بتاع الـ UserAdmin من هنا

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'specialization', 'consultation_fees']
    list_filter = ['department']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_by', 'created_at']
    search_fields = ['name', 'phone']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_number', 'patient', 'status', 'date_time']
    list_filter = ['status', 'date_time']
    search_fields = ['appointment_number', 'patient__name']

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'blood_pressure', 'temperature', 'updated_at']

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    search_fields = ['name']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'created_at']

@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'medicine', 'dosage', 'duration']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'patient', 'amount', 'status']
    list_filter = ['status']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'patient', 'amount', 'is_paid', 'due_date']
    list_filter = ['is_paid']

@admin.register(ClinicSettings)
class ClinicSettingsAdmin(admin.ModelAdmin):
    list_display = ['clinic_name', 'currency', 'timezone']