# core/apps.py
from django.apps import AppConfig
import sys
import django

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        """Applique les monkey patches APRÈS le chargement des apps"""
        
        # 1. Patch pour ugettext_lazy
        from django.utils.translation import gettext_lazy
        if not hasattr(django.utils.translation, 'ugettext_lazy'):
            django.utils.translation.ugettext_lazy = gettext_lazy
            sys.modules['django.utils.translation'].ugettext_lazy = gettext_lazy
            print("✓ Patch ugettext_lazy appliqué")
        
        # 2. Patch pour django.core.urlresolvers (si nécessaire)
        try:
            from django import urls
            class MockUrlresolvers:
                def __getattr__(self, name):
                    return getattr(urls, name)
            
            if 'django.core.urlresolvers' not in sys.modules:
                sys.modules['django.core.urlresolvers'] = MockUrlresolvers()
                print("✓ Patch urlresolvers appliqué")
        except ImportError:
            pass