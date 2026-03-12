from django.contrib import admin
from .models import Article, ArticleCategorie

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