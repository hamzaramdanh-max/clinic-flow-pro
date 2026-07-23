from django.db import models
from .base import BaseModel
from .appointment import Appointment
from .patient import Patient

class Payment(BaseModel):
    class PaymentStatus(models.TextChoices):
        UNPAID = "Unpaid", "Unpaid"
        PAID = "Paid", "Paid"
        REFUNDED = "Refunded", "Refunded"

    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments')
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_invoice = Payment.objects.all().order_by('-created_at').first()
            if last_invoice and last_invoice.invoice_number.startswith('INV-'):
                last_num = int(last_invoice.invoice_number.split('-')[1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.invoice_number = f"INV-{new_num:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - {self.patient.name}"