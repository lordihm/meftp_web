# core/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import ElementMenu

class ElementMenuAdmin(admin.ModelAdmin):
    list_display = ['titre', 'parent', 'ordre', 'actif', 'apercu']
    list_editable = ['ordre', 'actif']
    list_filter = ['actif', 'parent']
    search_fields = ['titre']
    ordering = ['parent__id', 'ordre']
    
    # Configuration des champs dans le formulaire
    fieldsets = (
        ('Informations générales', {
            'fields': ('titre', 'parent', 'ordre', 'actif')
        }),
        ('Destination du lien', {
            'fields': ('url_externe', 'page_cms'),
            'description': 'Choisissez une URL externe OU une page CMS'
        }),
    )
    
    def apercu(self, obj):
        """Affiche un aperçu du lien"""
        url = obj.get_absolute_url()
        if url and url != '#':
            return format_html('<a href="{}" target="_blank">🔗 Voir</a>', url)
        return "❌ Lien invalide"
    apercu.short_description = "Aperçu"

admin.site.register(ElementMenu, ElementMenuAdmin)