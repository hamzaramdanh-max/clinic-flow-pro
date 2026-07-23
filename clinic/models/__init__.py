from .base import BaseModel
from .department import Department
from .doctor import Doctor
from .patient import Patient
from .appointment import Appointment
from .medical_record import MedicalRecord
from .medicine import Medicine
from .prescription import Prescription, PrescriptionItem
from .payment import Payment
from .invoice import Invoice  # <--- السطر ده هو اللي كان ناقص
from .settings import ClinicSettings