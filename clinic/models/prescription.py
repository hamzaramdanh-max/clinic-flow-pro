from django.db import models
from .base import BaseModel
from .appointment import Appointment
from .medicine import Medicine

class Prescription(BaseModel):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    notes = models.TextField(blank=True, help_text="ملاحظات الدكتور")

    def __str__(self):
        return f"Prescription for {self.appointment.patient.name}"

# جدول فرعي عشان الروشتة الواحدة ممكن يكون فيها كذا دواء بجرعات مختلفة
class PrescriptionItem(BaseModel):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=255, help_text="مثال: حباية كل 8 ساعات")
    duration = models.CharField(max_length=100, help_text="مثال: لمدة 5 أيام", blank=True)

    def __str__(self):
        return f"{self.medicine.name} - {self.dosage}"