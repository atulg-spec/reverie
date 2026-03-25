from .models import SiteSettings

def site_settings(request):
    return {
        'settings': SiteSettings.objects.first()
    }

def user_location(request):
    return {
        'user_state': request.session.get('user_state'),
        'user_city': request.session.get('user_city'),
    }
