from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # عشان يظهرلك اسم اليوزر والدور بتاعه (دكتور ولا ريسبشن) من بره
    list_display = ('username', 'email', 'role', 'is_staff')
    
    # عشان تقدر تعدل الدور ورقم التليفون من جوه
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)