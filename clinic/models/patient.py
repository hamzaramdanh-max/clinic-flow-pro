from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .base import BaseModel


class Patient(BaseModel): 
    name = models.CharField(max_length=255, verbose_name=_("Patient Name"))
    phone = models.CharField(max_length=20, db_index=True, verbose_name=_("Phone Number"))
    email = models.EmailField(
        unique=True, 
        blank=True, 
        null=True, 
        db_index=True,
        verbose_name=_("Email")
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='patients_created',
        verbose_name=_("Created By")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")