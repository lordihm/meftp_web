# core/context_processors.py
from .models import Logo

def logo_du_site(request):
    try:
        config = Logo.objects.first()
    except:
        config = None
    return {'logo_site': config}