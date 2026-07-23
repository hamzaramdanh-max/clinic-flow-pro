from .models import ClinicSettings


def clinic_globals(request):
    try:
        settings = ClinicSettings.get_settings()
    except:
        settings = None

    return {
        'clinic_settings': settings,
        'currency': settings.currency if settings else '$',
    }