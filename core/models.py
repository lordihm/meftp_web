from django.db import models
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from django.utils import timezone
from cms.models import Page
from django.db import models
from django.utils import timezone
from cms.models import Page

#======= LOGO ET NOMS DU SITE =======#
class Logo(models.Model):
    logo = FilerImageField(verbose_name="Logo", on_delete=models.SET_NULL, null=True, blank=True)
    
    # Nom court sur 3 lignes
    nom_court_L1 = models.CharField(
        max_length=40, 
        default="République du Niger",
        verbose_name="Nom court (Première ligne)",
    )
    nom_court_L2 = models.CharField(
        max_length=40, 
        default="Ministère de l'Enseignement et de la",
        verbose_name="Nom court (Deuxième ligne)",
    )
    nom_court_L3 = models.CharField(
        max_length=40, 
        default="Formation Techniques et Professionnels",
        verbose_name="Nom court (Troisième ligne)",
    )

    nom_complet = models.CharField(
        max_length=200, 
        default="Ministère de l'Enseignement et de la Formation Techniques et Professionnels",
        verbose_name="Nom complet"
    )
    
    class Meta:
        verbose_name = "Logo du site"
        verbose_name_plural = "Logos du site"
    
    def __str__(self):
        return "Logo du site"

#======= ARTICLES D'ACTUALITÉS =======#
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

#======= CARROUSEL TEXTE AVEC IMAGE =======#

class SlideTexteFondPlugin(CMSPlugin):
    """Plugin pour un slide avec texte et image de fond"""
    titre = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Titre"
    )
    sous_titre = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Sous-titre"
    )
    texte = models.TextField(
        blank=True,
        verbose_name="Texte (HTML autorisé)"
    )
    image_fond = FilerImageField(
        verbose_name="Image de fond",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Image qui sera affichée en arrière-plan"
    )
    bouton_texte = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Texte du bouton"
    )
    bouton_lien = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Lien du bouton"
    )
    hauteur = models.CharField(
        max_length=20,
        default="600px",
        verbose_name="Hauteur du slide",
        help_text="Ex: 600px, 80vh, 100%"
    )
    
    class Meta:
        verbose_name = "Slide texte avec fond"
        verbose_name_plural = "Slides texte avec fond"
    
    def __str__(self):
        return self.titre or "Slide sans titre"