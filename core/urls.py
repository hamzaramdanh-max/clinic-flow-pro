from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # 🏠 Redirect الصفحة الرئيسية إلى Login
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    
    path('admin/', admin.site.urls),
    
    # 🌍 URL لتبديل اللغة (Django built-in)
    path('i18n/', include('django.conf.urls.i18n')),
    
    # ده السطر اللي بيربط المشروع بالـ accounts
    path('accounts/', include('accounts.urls')),
]

# 🖼️ عشان الصور والملفات المرفوعة تشتغل في Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)