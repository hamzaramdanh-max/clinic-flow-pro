from django.db import models
from .base import BaseModel
from .patient import Patient

class MedicalRecord(BaseModel):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='medical_record')
    
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    blood_pressure = models.CharField(max_length=20, null=True, blank=True, help_text="e.g. 120/80")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Temp in Celsius")
    
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Record for {self.patient.name}"