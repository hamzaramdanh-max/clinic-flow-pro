from django import forms
from django.utils.translation import gettext_lazy as _
from clinic.models import Patient, Doctor, Appointment, Medicine, Invoice, ClinicSettings


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'phone', 'email']
        labels = {
            'name': _('Patient Name'),
            'phone': _('Phone Number'),
            'email': _('Email (Optional)'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter patient name')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter phone number')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter email address')}),
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user', 'department', 'specialization', 'consultation_fees']
        labels = {
            'user': _('Select User Account'),
            'department': _('Department'),
            'specialization': _('Specialization'),
            'consultation_fees': _('Consultation Fees'),
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g. Cardiologist')}),
            'consultation_fees': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('e.g. 500')}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date_time', 'status']
        labels = {
            'patient': _('Select Patient'),
            'doctor': _('Select Doctor'),
            'date_time': _('Date & Time'),
            'status': _('Status'),
        }
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'date_time': forms.TextInput(attrs={'class': 'form-control bg-white', 'placeholder': _('Select Date & Time...')}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'price', 'stock', 'expiry_date']
        labels = {
            'name': _('Medicine Name'),
            'price': _('Price'),
            'stock': _('Stock Quantity'),
            'expiry_date': _('Expiry Date'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Medicine Name')}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['patient', 'doctor', 'amount', 'is_paid', 'due_date']
        labels = {
            'patient': _('Select Patient'),
            'doctor': _('Select Doctor'),
            'amount': _('Amount'),
            'is_paid': _('Mark as Paid'),
            'due_date': _('Due Date'),
        }
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('e.g. 500')}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }


# ==================== Settings Form ====================
class SettingsForm(forms.ModelForm):
    class Meta:
        model = ClinicSettings
        fields = [
            # Clinic Info
            'clinic_name', 'logo', 'address', 'phone', 'email', 'website',
            # Financial
            'currency', 'default_tax', 'default_discount', 'invoice_prefix',
            # Appearance
            'language', 'primary_color', 'dark_mode',
            # Notifications
            'enable_email_notifications', 'low_stock_threshold', 'enable_appointment_reminders',
            # SMTP
            'smtp_email', 'smtp_password', 'smtp_host', 'smtp_port',
            # System
            'timezone', 'working_hours_from', 'working_hours_to',
        ]
        labels = {
            'clinic_name': _('Clinic Name'),
            'logo': _('Logo'),
            'address': _('Address'),
            'phone': _('Phone'),
            'email': _('Email'),
            'website': _('Website'),
            'currency': _('Currency'),
            'default_tax': _('Default Tax (%)'),
            'default_discount': _('Default Discount (%)'),
            'invoice_prefix': _('Invoice Prefix'),
            'language': _('Language'),
            'primary_color': _('Primary Color'),
            'dark_mode': _('Dark Mode'),
            'enable_email_notifications': _('Enable Email Notifications'),
            'low_stock_threshold': _('Low Stock Alert Threshold'),
            'enable_appointment_reminders': _('Enable Appointment Reminders'),
            'smtp_email': _('SMTP Email'),
            'smtp_password': _('SMTP Password'),
            'smtp_host': _('SMTP Host'),
            'smtp_port': _('SMTP Port'),
            'timezone': _('Timezone'),
            'working_hours_from': _('Working Hours From'),
            'working_hours_to': _('Working Hours To'),
        }
        widgets = {
            'clinic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g. ClinicFlow Pro')}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Full clinic address')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+20 100 000 0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'info@clinic.com'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourclinic.com'}),
            
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'default_tax': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'default_discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'invoice_prefix': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'INV-'}),
            
            'language': forms.Select(attrs={'class': 'form-select'}),
            'primary_color': forms.TextInput(attrs={'class': 'form-control form-control-color', 'type': 'color'}),
            'dark_mode': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'enable_email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
            'enable_appointment_reminders': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            'smtp_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your-email@gmail.com'}),
            'smtp_password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('App Password'), 'render_value': True}),
            'smtp_host': forms.TextInput(attrs={'class': 'form-control'}),
            'smtp_port': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'timezone': forms.TextInput(attrs={'class': 'form-control'}),
            'working_hours_from': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'working_hours_to': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }