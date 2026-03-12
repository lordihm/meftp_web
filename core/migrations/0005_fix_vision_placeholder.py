from django.db import migrations
from cms.models import Page, Placeholder
from cms.api import add_plugin

def fix_vision_placeholder(apps, schema_editor):
    try:
        Page = apps.get_model('cms', 'Page')
        Placeholder = apps.get_model('cms', 'Placeholder')
        
        home_page = Page.objects.get(title_set__title="Accueil")
        
        # Nettoyer et recréer le placeholder
        home_page.placeholders.filter(slot='vision_text').delete()
        new_ph = Placeholder.objects.create(slot='vision_text')
        home_page.placeholders.add(new_ph)
        
        # Ajouter un texte par défaut (optionnel)
        if 'fr' in [lang[0] for lang in settings.LANGUAGES]:
            add_plugin(
                new_ph,
                'TextPlugin',
                'fr',
                body='<p class="lead">Développer des ressources humaines qualifiées pour un Niger émergent.</p>'
            )
            
    except Exception as e:
        print(f"Erreur: {e}")

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),  # Adaptez à votre dernière migration
    ]

    operations = [
        migrations.RunPython(fix_vision_placeholder),
    ]