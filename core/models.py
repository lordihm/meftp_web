from django.db import models
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from django.urls import reverse
from cms.models import Page

class Testimonial(models.Model):
    """Modèle pour les témoignages"""
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class TestimonialPlugin(CMSPlugin):
    """Plugin pour afficher les témoignages"""
    title = models.CharField(max_length=100, blank=True)
    limit = models.PositiveIntegerField(default=5, help_text="Nombre de témoignages à afficher")

    def __str__(self):
        return self.title or "Témoignages" 

class ElementMenu(models.Model):
    """Modèle personnalisé pour gérer les menus sans dépendre de django-menus"""
    titre = models.CharField(
        max_length=100, 
        verbose_name="Titre du menu"
    )
    
    # Choix entre URL externe ou page CMS interne
    url_externe = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="URL externe",
        help_text="Laissez vide pour utiliser une page CMS"
    )
    
    page_cms = models.ForeignKey(
        Page, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Page CMS",
        help_text="Ou sélectionnez une page du site"
    )
    
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='enfants',
        verbose_name="Menu parent"
    )
    
    ordre = models.IntegerField(
        default=0, 
        verbose_name="Ordre d'affichage"
    )
    
    actif = models.BooleanField(
        default=True, 
        verbose_name="Actif",
        help_text="Décocher pour masquer temporairement"
    )
    
    class Meta:
        ordering = ['parent__id', 'ordre']
        verbose_name = "Élément de menu"
        verbose_name_plural = "Éléments de menu"
    
    def __str__(self):
        return self.titre
    
    def get_absolute_url(self):
        """Retourne l'URL appropriée"""
        if self.page_cms and self.page_cms.is_published('fr'):
            return self.page_cms.get_absolute_url()
        return self.url_externe or '#'
    
    def get_children(self):
        """Retourne les enfants actifs triés"""
        return self.enfants.filter(actif=True).order_by('ordre')
    
    def has_children(self):
        """Vérifie si l'élément a des enfants actifs"""
        return self.get_children().exists()
        if self.page_cms:
            return self.page_cms.get_absolute_url()
        return self.url

# core/models.py
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
    couleur = models.CharField(max_length=7, default="#F97316",
                              help_text="Code hexadécimal (ex: #F97316)")
    
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
    galerie_images = models.ManyToManyField(
        'filer.Image', 
        blank=True,
        related_name='articles'
    )
    document_joint = FilerFileField(
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    date_publication = models.DateTimeField(default=timezone.now)
    date_evenement = models.DateTimeField(null=True, blank=True)
    lieu = models.CharField(max_length=100, blank=True)
    auteur = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)
    
    # Catégorisation
    categorie = models.ForeignKey(
        'ArticleCategorie', 
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    tags = models.CharField(max_length=200, blank=True, 
                           help_text="Séparés par des virgules")
    
    # Métadonnées
    est_publie = models.BooleanField(default=True)
    est_a_la_une = models.BooleanField(default=False)
    vue_count = models.IntegerField(default=0)
    
    # Relations CMS
    page_liee = models.ForeignKey(
        Page, null=True, blank=True,
        on_delete=models.SET_NULL,
        help_text="Page CMS associée (optionnel)"
    )
    
    class Meta:
        ordering = ['-date_publication', '-est_a_la_une']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
    
    def __str__(self):
        return self.titre
    
    def get_absolute_url(self):
        if self.page_liee:
            return self.page_liee.get_absolute_url()
        return f"/actualites/{self.slug}/"
    
    def increment_view_count(self):
        self.vue_count += 1
        self.save()