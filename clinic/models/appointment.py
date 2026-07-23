from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .patient import Patient
from .doctor import Doctor


class Appointment(BaseModel):
    class AppointmentStatus(models.TextChoices):
        PENDING = "Pending", _("Pending")
        CONFIRMED = "Confirmed", _("Confirmed")
        COMPLETED = "Completed", _("Completed")
        CANCELLED = "Cancelled", _("Cancelled")

    appointment_number = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='appointments',
        verbose_name=_("Patient")
    )
    
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name='appointments', 
        null=True,
        verbose_name=_("Doctor")
    )
    
    status = models.CharField(
        max_length=20, 
        choices=AppointmentStatus.choices, 
        default=AppointmentStatus.PENDING,
        verbose_name=_("Status")
    )
    date_time = models.DateTimeField(verbose_name=_("Date & Time"))

    def save(self, *args, **kwargs):
        if not self.appointment_number:
            last_appointment = Appointment.objects.all().order_by('-created_at').first()
            if last_appointment and last_appointment.appointment_number.startswith('APT-'):
                last_num = int(last_appointment.appointment_number.split('-')[1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.appointment_number = f"APT-{new_num:05d}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.appointment_number} - {self.patient.name}"

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")