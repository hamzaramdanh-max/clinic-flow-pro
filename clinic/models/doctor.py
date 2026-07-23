from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .base import BaseModel
from .department import Department


class Doctor(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='doctor_profile',
        verbose_name=_("User Account")
    )
    
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='doctors',
        verbose_name=_("Department")
    )
    
    specialization = models.CharField(max_length=255, verbose_name=_("Specialization"))
    consultation_fees = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0.00,
        verbose_name=_("Consultation Fees")
    )

    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username} - {self.specialization}"

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")