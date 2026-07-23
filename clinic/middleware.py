"""
Custom Middleware for ClinicFlow Pro
"""
from django.utils import translation
from clinic.models.settings import ClinicSettings


class ForceClinicLanguageMiddleware:
    """
    Middleware يجبر Django يستخدم اللغة المختارة في إعدادات العيادة
    بدلاً من لغة المتصفح
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            # جيب اللغة من إعدادات العيادة
            settings_obj = ClinicSettings.get_settings()
            language = settings_obj.language
            
            # فعّلها في Django
            if language in ['en', 'ar']:
                translation.activate(language)
                request.LANGUAGE_CODE = language
        except Exception:
            # لو حصل أي error، سيب Django يشتغل عادي
            pass
        
        response = self.get_response(request)
        return response