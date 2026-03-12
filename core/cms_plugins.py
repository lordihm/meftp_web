# core/cms_plugins.py - VERSION CORRECTE (pas de doublon)
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext_lazy as _
from .models import Article, ArticleCategorie

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

# ATTENTION : Ne PAS réenregistrer les plugins ici !
# plugin_pool.register_plugin(ArticlesRecentsPlugin)  <- Supprimez ces lignes si elles existent
# plugin_pool.register_plugin(ArticlesParCategoriePlugin)  <- Supprimez ces lignes