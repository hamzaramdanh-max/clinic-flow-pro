from django.db import models
from django.utils.translation import gettext_lazy as _
from .base import BaseModel


class Medicine(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Medicine Name"))
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name=_("Price")
    )
    stock = models.IntegerField(default=0, verbose_name=_("Stock Quantity"))
    expiry_date = models.DateField(null=True, blank=True, verbose_name=_("Expiry Date"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Medicine")
        verbose_name_plural = _("Medicines")