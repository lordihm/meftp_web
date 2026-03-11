from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import Testimonial, TestimonialPlugin
from cms.models.pluginmodel import CMSPlugin
from .models import Article, ArticleCategorie

@plugin_pool.register_plugin
class TestimonialPluginPublisher(CMSPluginBase):
    model = TestimonialPlugin
    name = _("Témoignages")
    render_template = "core/testimonials.html"
    cache = False
    
    def render(self, context, instance, placeholder):
        context.update({
            'testimonials': Testimonial.objects.all()[:instance.limit],
            'title': instance.title,
        })
        return context

# core/cms_plugins.py
class ArticlesRecentsPlugin(CMSPluginBase):
    model = CMSPlugin  # ⬅️ CORRIGÉ (et non CMSPluginBase)
    name = _("Articles récents")
    render_template = "core/articles_recents.html"
    cache = False
    module = "ME/FT/P"
    
    def render(self, context, instance, placeholder):
        context.update({
            'articles': Article.objects.filter(est_publie=True)[:3],
            'placeholder': placeholder
        })
        return context

class ArticlesParCategoriePlugin(CMSPluginBase):
    model = CMSPlugin  # ⬅️ CORRIGÉ
    name = _("Articles par catégorie")
    render_template = "core/articles_categorie.html"
    cache = False
    module = "ME/FT/P"
    
    def render(self, context, instance, placeholder):
        context.update({
            'categories': ArticleCategorie.objects.all(),
            'placeholder': placeholder
        })
        return context

class ArticleAvecImagePlugin(CMSPluginBase):
    model = CMSPlugin  # ⬅️ CORRIGÉ
    name = _("Article à la une")
    render_template = "core/article_card.html"
    cache = False
    module = "ME/FT/P"
    
    def render(self, context, instance, placeholder):
        article = Article.objects.filter(est_publie=True, est_a_la_une=True).first()
        context.update({
            'article': article,
            'placeholder': placeholder
        })
        return context

# Enregistrement des plugins
plugin_pool.register_plugin(ArticlesRecentsPlugin)
plugin_pool.register_plugin(ArticlesParCategoriePlugin)
plugin_pool.register_plugin(ArticleAvecImagePlugin)