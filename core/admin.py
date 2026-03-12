# core/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Article, ArticleCategorie, Logo

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['nom_court_complet', 'nom_complet', 'logo_preview']
    fieldsets = (
        ('Logo', {
            'fields': ('logo', 'logo_preview'),
            'description': 'Uploader le logo du site (format recommandé: PNG avec fond transparent)'
        }),
        ('Nom court (3 lignes)', {
            'fields': ('nom_court_L1', 'nom_court_L2', 'nom_court_L3'),
            'description': 'Saisissez les trois lignes du nom court'
        }),
        ('Nom complet', {
            'fields': ('nom_complet',),
            'description': 'Nom complet de l\'institution (affiché dans le footer)'
        }),
    )
    readonly_fields = ['logo_preview']
    
    def logo_preview(self, obj):
        """Affiche un aperçu du logo dans l'admin"""
        if obj and obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px; border: 1px solid #ddd; border-radius: 4px; padding: 5px;" />',
                obj.logo.url
            )
        return "Aucun logo"
    logo_preview.short_description = "Aperçu"
    
    def nom_court_complet(self, obj):
        """Affiche les 3 lignes du nom court dans l'admin"""
        if obj:
            return format_html(
                '{}<br>{}<br>{}',
                obj.nom_court_L1,
                obj.nom_court_L2,
                obj.nom_court_L3
            )
        return "-"
    nom_court_complet.short_description = "Nom court (3 lignes)"

# Le reste inchangé
@admin.register(ArticleCategorie)
class ArticleCategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'couleur']
    prepopulated_fields = {'slug': ('nom',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'date_publication', 'est_publie', 'est_a_la_une']
    list_filter = ['categorie', 'est_publie', 'est_a_la_une']
    search_fields = ['titre', 'chapeau']
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'