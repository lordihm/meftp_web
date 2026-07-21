# core/cms_plugins.py - VERSION CORRECTE (pas de doublon)
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext_lazy as _
from .models import Article, ArticleCategorie
from .models import SlideTexteFondPlugin

#======= PLUGINS CMS =======#
@plugin_pool.register_plugin
class ArticlesRecentsPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Articles récents")
    render_template = "core/articles_recents.html"
    cache = False
    module = "ME/FT/P"
    
    def render(self, context, instance, placeholder):
        context.update({
            'articles': Article.objects.filter(est_publie=True)[:3],
        })
        return context

@plugin_pool.register_plugin
class ArticlesParCategoriePlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Articles par catégorie")
    render_template = "core/articles_categorie.html"
    cache = False
    module = "ME/FT/P"
    
    def render(self, context, instance, placeholder):
        context.update({
            'categories': ArticleCategorie.objects.all(),
        })
        return context

#======= CARROUSEL TEXTE AVEC IMAGE DE FOND =======#
@plugin_pool.register_plugin
class SlideTexteFondPluginPublisher(CMSPluginBase):
    model = SlideTexteFondPlugin  # ← Nom corrigé
    name = _("Slide texte avec fond")
    render_template = "Site_web/slide_texte_fond.html"
    cache = False
    module = "ME/FTP"
    
    fieldsets = (
        ('Texte', {
            'fields': ('titre', 'sous_titre', 'texte')
        }),
        ('Image de fond', {
            'fields': ('image_fond',),
            'description': 'Image affichée en arrière-plan (format paysage recommandé)'
        }),
        ('Bouton (optionnel)', {
            'fields': ('bouton_texte', 'bouton_lien'),
            'classes': ('collapse',)
        }),
        ('Dimensions', {
            'fields': ('hauteur',),
            'classes': ('collapse',)
        }),
    )
    
    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'placeholder': placeholder
        })
        return context
    