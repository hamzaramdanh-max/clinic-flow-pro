from django.db import models
from .base import BaseModel


class ClinicSettings(BaseModel):
    # ==================== Clinic Info ====================
    clinic_name = models.CharField(max_length=255, default="ClinicFlow Pro")
    logo = models.ImageField(upload_to='clinic_logos/', null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    
    # ==================== Financial Settings ====================
    CURRENCY_CHOICES = (
        ('$', 'USD - US Dollar ($)'),
        ('€', 'EUR - Euro (€)'),
        ('£', 'GBP - British Pound (£)'),
        ('EGP', 'EGP - Egyptian Pound'),
        ('SAR', 'SAR - Saudi Riyal'),
        ('AED', 'AED - UAE Dirham'),
    )
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default="EGP")
    default_tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Default tax percentage (%)")
    default_discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Default discount percentage (%)")
    invoice_prefix = models.CharField(max_length=10, default="INV-")
    next_invoice_number = models.IntegerField(default=1001)
    
    # ==================== Appearance ====================
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('ar', 'العربية'),
    )
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    primary_color = models.CharField(max_length=7, default="#0d6efd", help_text="Hex color code")
    dark_mode = models.BooleanField(default=False)
    
    # ==================== Notifications ====================
    enable_email_notifications = models.BooleanField(default=False)
    low_stock_threshold = models.IntegerField(default=10, help_text="Alert when medicine stock is below this number")
    enable_appointment_reminders = models.BooleanField(default=True)
    
    # ==================== SMTP Settings ====================
    smtp_email = models.CharField(max_length=255, blank=True, null=True)
    smtp_password = models.CharField(max_length=255, blank=True, null=True)
    smtp_host = models.CharField(max_length=100, default="smtp.gmail.com", blank=True)
    smtp_port = models.IntegerField(default=587)
    
    # ==================== System ====================
    timezone = models.CharField(max_length=50, default="Africa/Cairo")
    working_hours_from = models.TimeField(default="09:00")
    working_hours_to = models.TimeField(default="21:00")

    def __str__(self):
        return f"Settings: {self.clinic_name}"
    
    def save(self, *args, **kwargs):
        # Singleton Pattern - صف واحد بس
        if not self.pk and ClinicSettings.objects.exists():
            existing = ClinicSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = "Clinic Setting"
        verbose_name_plural = "Clinic Settings"