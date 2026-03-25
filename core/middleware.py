import requests
from django.conf import settings

class LocationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Manual Override check (via query param)
        set_state = request.GET.get('set_state')
        if set_state:
            request.session['user_state'] = set_state
            # Option to also set a cookie or just rely on session
        
        # 2. Location Detection (if not already set in session)
        if 'user_state' not in request.session:
            try:
                # Get client IP
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                # Localhost check for development
                if ip in ['127.0.0.1', '::1', 'localhost']:
                    # Default for local testing if needed, or leave None
                    request.session['user_state'] = None
                else:
                    # External API call (ip-api.com is free for non-commercial)
                    response = requests.get(f'http://ip-api.com/json/{ip}', timeout=2)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('status') == 'success':
                            request.session['user_state'] = data.get('regionName') # E.g. "Uttar Pradesh"
                            request.session['user_city'] = data.get('city')
                        else:
                            request.session['user_state'] = None
                    else:
                        request.session['user_state'] = None
            except Exception:
                request.session['user_state'] = None

        response = self.get_response(request)
        return response
