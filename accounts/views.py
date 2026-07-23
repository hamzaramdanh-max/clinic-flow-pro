from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils.translation import gettext_lazy as _

from .decorators import role_required
from .forms import PatientForm, DoctorForm, AppointmentForm, MedicineForm, InvoiceForm, SettingsForm
from clinic.models import Patient, Doctor, Appointment, Invoice, Medicine, ClinicSettings


# ================= Dashboard =================
@login_required
def dashboard(request):
    context = {
        'patients_count': Patient.objects.count(),
        'doctors_count': Doctor.objects.count(),
        'appointments_count': Appointment.objects.count(),
        'invoices_count': Invoice.objects.count(),
        'recent_patients': Patient.objects.order_by('-created_at')[:5],
        'recent_appointments': Appointment.objects.order_by('-created_at')[:5],
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


# ================= Settings =================
@login_required
def settings_view(request):
    settings_obj = ClinicSettings.get_settings()

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, _('Settings updated successfully! ⚙️'))
            return redirect('accounts:settings')
        else:
            messages.error(request, _('Please correct the errors below.'))
    else:
        form = SettingsForm(instance=settings_obj)

    return render(request, 'accounts/settings.html', {
        'form': form,
        'settings': settings_obj
    })


# ================= Role Panels =================
@login_required
@role_required(['Doctor'])
def doctor_panel(request):
    return HttpResponse("<h1 style='color:blue; text-align:center; margin-top:50px;'>👨‍⚕️ Welcome Doctor!</h1>")


@login_required
@role_required(['Receptionist'])
def reception_panel(request):
    return HttpResponse("<h1 style='color:green; text-align:center; margin-top:50px;'>💻 Welcome Receptionist!</h1>")


# ================= Patients =================
@login_required
def patients_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.all().order_by('-created_at')

    if query:
        patients = patients.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'accounts/patients_list.html', {
        'patients': patients,
        'query': query
    })


@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            messages.success(request, _('Patient Added Successfully! ✅'))
            return redirect('accounts:patients_list')
    else:
        form = PatientForm()
    return render(request, 'accounts/add_patient.html', {'form': form, 'title': _('Add New Patient')})


@login_required
def view_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')
    invoices = Invoice.objects.filter(patient=patient).order_by('-created_at')
    context = {
        'patient': patient,
        'appointments': appointments,
        'invoices': invoices
    }
    return render(request, 'accounts/view_patient.html', context)


@login_required
def edit_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, _('Patient Updated Successfully! ✏️'))
            return redirect('accounts:patients_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'accounts/add_patient.html', {'form': form, 'title': _('Edit Patient')})


@login_required
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, _('Patient Deleted Successfully! 🗑️'))
        return redirect('accounts:patients_list')
    return render(request, 'accounts/delete_confirm.html', {
        'object_name': patient.name,
        'object_type': _('patient'),
        'cancel_url': 'accounts:patients_list'
    })


# ================= Doctors =================
@login_required
def doctors_list(request):
    query = request.GET.get('q', '')
    doctors = Doctor.objects.all()

    if query:
        doctors = doctors.filter(
            Q(user__username__icontains=query) |
            Q(specialization__icontains=query)
        )

    return render(request, 'accounts/doctors_list.html', {
        'doctors': doctors,
        'query': query
    })


@login_required
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Doctor Added Successfully! 👨‍⚕️'))
            return redirect('accounts:doctors_list')
    else:
        form = DoctorForm()
    return render(request, 'accounts/add_doctor.html', {'form': form, 'title': _('Add New Doctor')})


@login_required
def view_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date_time')[:10]
    total_appointments = Appointment.objects.filter(doctor=doctor).count()
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'total_appointments': total_appointments,
    }
    return render(request, 'accounts/view_doctor.html', context)


@login_required
def edit_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, _('Doctor Updated Successfully! ✏️'))
            return redirect('accounts:doctors_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'accounts/add_doctor.html', {'form': form, 'title': _('Edit Doctor')})


@login_required
def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        messages.success(request, _('Doctor Deleted Successfully! 🗑️'))
        return redirect('accounts:doctors_list')
    return render(request, 'accounts/delete_confirm.html', {
        'object_name': f"Dr. {doctor.user.username}",
        'object_type': _('doctor'),
        'cancel_url': 'accounts:doctors_list'
    })


# ================= Appointments =================
@login_required
def appointments_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.all().order_by('-date_time')

    if query:
        appointments = appointments.filter(
            Q(patient__name__icontains=query) |
            Q(doctor__user__username__icontains=query)
        )

    if status_filter:
        appointments = appointments.filter(status=status_filter)

    return render(request, 'accounts/appointments_list.html', {
        'appointments': appointments,
        'query': query,
        'status_filter': status_filter,
    })


@login_required
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Appointment Booked Successfully! 📅'))
            return redirect('accounts:appointments_list')
    else:
        form = AppointmentForm()
    return render(request, 'accounts/add_appointment.html', {'form': form, 'title': _('Book New Appointment')})


@login_required
def view_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'accounts/view_appointment.html', {'appointment': appointment})


@login_required
def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, _('Appointment Updated Successfully! ✏️'))
            return redirect('accounts:appointments_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'accounts/add_appointment.html', {'form': form, 'title': _('Edit Appointment')})


@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, _('Appointment Canceled Successfully! 🗑️'))
        return redirect('accounts:appointments_list')
    return render(request, 'accounts/delete_confirm.html', {
        'object_name': appointment.appointment_number,
        'object_type': _('appointment'),
        'cancel_url': 'accounts:appointments_list'
    })


# ================= Medicines =================
@login_required
def medicines_list(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')
    medicines = Medicine.objects.all().order_by('name')

    if query:
        medicines = medicines.filter(name__icontains=query)

    if filter_type == 'low_stock':
        medicines = medicines.filter(stock__lt=10)

    return render(request, 'accounts/medicines_list.html', {
        'medicines': medicines,
        'query': query,
        'filter_type': filter_type,
    })


@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Medicine Added Successfully! 💊'))
            return redirect('accounts:medicines_list')
    else:
        form = MedicineForm()
    return render(request, 'accounts/add_medicine.html', {'form': form, 'title': _('Add New Medicine')})


@login_required
def view_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    return render(request, 'accounts/view_medicine.html', {'medicine': medicine})


@login_required
def edit_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, _('Medicine Updated Successfully! ✏️'))
            return redirect('accounts:medicines_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'accounts/add_medicine.html', {'form': form, 'title': _('Edit Medicine')})


@login_required
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        medicine.delete()
        messages.success(request, _('Medicine Deleted Successfully! 🗑️'))
        return redirect('accounts:medicines_list')
    return render(request, 'accounts/delete_confirm.html', {
        'object_name': medicine.name,
        'object_type': _('medicine'),
        'cancel_url': 'accounts:medicines_list'
    })


# ================= Invoices =================
@login_required
def invoices_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    invoices = Invoice.objects.all().order_by('-created_at')

    if query:
        invoices = invoices.filter(
            Q(invoice_number__icontains=query) |
            Q(patient__name__icontains=query)
        )

    if status_filter == 'paid':
        invoices = invoices.filter(is_paid=True)
    elif status_filter == 'unpaid':
        invoices = invoices.filter(is_paid=False)

    return render(request, 'accounts/invoices_list.html', {
        'invoices': invoices,
        'query': query,
        'status_filter': status_filter,
    })


@login_required
def add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            if not invoice.invoice_number:
                invoice.invoice_number = f"INV-{Invoice.objects.count() + 1001}"
            invoice.save()
            messages.success(request, _('Invoice Created Successfully! 💰'))
            return redirect('accounts:invoices_list')
    else:
        form = InvoiceForm()
    return render(request, 'accounts/add_invoice.html', {'form': form, 'title': _('Create New Invoice')})


@login_required
def view_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'accounts/view_invoice.html', {'invoice': invoice})


@login_required
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, _('Invoice Updated Successfully! ✏️'))
            return redirect('accounts:invoices_list')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'accounts/add_invoice.html', {'form': form, 'title': _('Edit Invoice')})


@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, _('Invoice Deleted Successfully! 🗑️'))
        return redirect('accounts:invoices_list')
    return render(request, 'accounts/delete_confirm.html', {
        'object_name': invoice.invoice_number,
        'object_type': _('invoice'),
        'cancel_url': 'accounts:invoices_list'
    })


@login_required
def print_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    settings_obj = ClinicSettings.get_settings()
    context = {
        'invoice': invoice,
        'settings': settings_obj,
    }
    return render(request, 'accounts/print_invoice.html', context)


# ================= Reports =================
@login_required
def reports(request):
    total_revenue = Invoice.objects.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
    unpaid_revenue = Invoice.objects.filter(is_paid=False).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_revenue': total_revenue,
        'unpaid_revenue': unpaid_revenue,
        'total_appointments': Appointment.objects.count(),
        'total_medicines': Medicine.objects.count(),
        'low_stock_medicines': Medicine.objects.filter(stock__lt=10).count(),
        'recent_appointments': Appointment.objects.all().order_by('-date_time')[:5],
        'recent_invoices': Invoice.objects.all().order_by('-created_at')[:5],
        'pending_appts': Appointment.objects.filter(status='Pending').count(),
        'confirmed_appts': Appointment.objects.filter(status='Confirmed').count(),
        'completed_appts': Appointment.objects.filter(status='Completed').count(),
        'cancelled_appts': Appointment.objects.filter(status='Cancelled').count(),
    }
    return render(request, 'accounts/reports.html', context)


# ==================================================================
# 🌍 Change Language View
# ==================================================================
def change_language(request, lang_code):
    """
    View لتغيير لغة الموقع وحفظها في الداتابيز
    """
    if lang_code in ['en', 'ar']:
        settings_obj = ClinicSettings.get_settings()
        settings_obj.language = lang_code
        settings_obj.save()
        
        request.session['django_language'] = lang_code
        
        if lang_code == 'ar':
            messages.success(request, 'تم تغيير اللغة إلى العربية بنجاح ✅')
        else:
            messages.success(request, 'Language changed to English successfully ✅')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))