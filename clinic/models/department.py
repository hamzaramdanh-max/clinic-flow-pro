from django.db import models
from .base import BaseModel

class Department(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # مش هنضيف is_active لأننا ورثناها خلاص من الـ BaseModel

    def __str__(self):
        return self.name