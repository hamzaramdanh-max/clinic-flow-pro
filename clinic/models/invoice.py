from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .patient import Patient
from .doctor import Doctor


class Invoice(BaseModel):
    invoice_number = models.CharField(
        max_length=20, 
        unique=True, 
        blank=True,
        verbose_name=_("Invoice Number")
    )
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='invoices',
        verbose_name=_("Patient")
    )
    
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='invoices',
        verbose_name=_("Doctor")
    )
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name=_("Amount")
    )
    is_paid = models.BooleanField(default=False, verbose_name=_("Is Paid"))
    due_date = models.DateField(null=True, blank=True, verbose_name=_("Due Date"))

    def __str__(self):
        return f"{self.invoice_number} - {self.patient.name}"

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")