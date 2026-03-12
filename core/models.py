from django.db import models
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from django.utils import timezone
from cms.models import Page

class ArticleCategorie(models.Model):
    """Catégories pour les articles"""
    nom = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    couleur = models.CharField(max_length=7, default="#F97316")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.nom

class Article(models.Model):
    """Modèle pour les articles d'actualité"""
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    chapeau = models.TextField(max_length=300, blank=True)
    contenu = models.TextField()
    image_principale = FilerImageField(
        null=True, blank=True, 
        on_delete=models.SET_NULL,
        related_name='article_principal'
    )
    date_publication = models.DateTimeField(default=timezone.now)
    lieu = models.CharField(max_length=100, blank=True)
    auteur = models.CharField(max_length=100, blank=True)
    categorie = models.ForeignKey(
        ArticleCategorie, 
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    est_publie = models.BooleanField(default=True)
    est_a_la_une = models.BooleanField(default=False)
    vue_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date_publication', '-est_a_la_une']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
    
    def __str__(self):
        return self.titre
    
    def get_absolute_url(self):
        return f"/actualites/{self.slug}/"