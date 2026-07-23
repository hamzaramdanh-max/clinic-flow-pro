import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        DOCTOR = 'Doctor', 'Doctor'
        RECEPTIONIST = 'Receptionist', 'Receptionist'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.RECEPTIONIST)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.role}"