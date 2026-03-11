# core/menu.py - Version avancée avec méga-menu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from cms.models import Page

class MegaMenu(Menu):
    """
    Menu principal avec support des méga-menus
    """
    name = _("Menu principal")
    
    def get_nodes(self, request):
        nodes = []
        
        # 1. Accueil
        nodes.append(NavigationNode(
            _('Accueil'),
            '/',
            1,
            attr={'icon': 'bi-house'}
        ))
        
        # 2. Le Ministère (avec méga-menu)
        ministry_node = NavigationNode(
            _('Le Ministère'),
            '#',
            2,
            attr={
                'mega_menu': True,
                'columns': 4,
                'icon': 'bi-building'
            }
        )
        nodes.append(ministry_node)
        
        # Sous-menus du Ministère
        ministry_items = [
            (_('Mot du Ministre'), '/mot-du-ministre/', 21, 'bi-person-badge'),
            (_('Organigramme'), '/organigramme/', 22, 'bi-diagram-3'),
            (_('Cabinet'), '/cabinet/', 23, 'bi-briefcase'),
            (_('Directions Générales'), '/directions/', 24, 'bi-building-gear'),
            (_('Missions et Attributions'), '/missions/', 25, 'bi-bullseye'),
            (_('Textes Fondateurs'), '/textes-fondateurs/', 26, 'bi-file-text'),
            (_('Conseillers Techniques'), '/conseillers/', 27, 'bi-people'),
            (_('Services Régionaux'), '/services-regionaux/', 28, 'bi-geo-alt'),
            (_('Projets Stratégiques'), '/projets/', 29, 'bi-rocket'),
            (_('Partenaires'), '/partenaires/', 30, 'bi-handshake'),
            (_('Documents Administratifs'), '/documents/', 31, 'bi-folder'),
            (_('Annuaire Téléphonique'), '/annuaire/', 32, 'bi-telephone'),
        ]
        
        for title, url, node_id, icon in ministry_items:
            nodes.append(NavigationNode(
                title,
                url,
                node_id,
                2,  # parent_id = ministry_node.id
                attr={'icon': icon}
            ))
        
        # 3. Actualités & Médias (avec méga-menu)
        news_node = NavigationNode(
            _('Actualités & Médias'),
            '#',
            3,
            attr={
                'mega_menu': True,
                'columns': 3,
                'icon': 'bi-newspaper'
            }
        )
        nodes.append(news_node)
        
        news_items = [
            (_('Dernières actualités'), '/actualites/', 41, 'bi-calendar-event'),
            (_('Communiqués de presse'), '/communiques/', 42, 'bi-megaphone'),
            (_('Discours officiels'), '/discours/', 43, 'bi-mic'),
            (_('Galerie photos'), '/galerie/', 44, 'bi-images'),
            (_('Vidéos'), '/videos/', 45, 'bi-camera-video'),
            (_('Revue de presse'), '/revue-presse/', 46, 'bi-journal'),
            (_('Agenda du Ministre'), '/agenda/', 47, 'bi-calendar-week'),
            (_('Newsletter'), '/newsletter/', 48, 'bi-envelope'),
            (_('Podcasts'), '/podcasts/', 49, 'bi-podcast'),
        ]
        
        for title, url, node_id, icon in news_items:
            nodes.append(NavigationNode(
                title,
                url,
                node_id,
                3,  # parent_id = news_node.id
                attr={'icon': icon}
            ))
        
        # 4. Textes & Lois
        texts_node = NavigationNode(
            _('Textes & Lois'),
            '#',
            4,
            attr={'icon': 'bi-file-earmark-law'}
        )
        nodes.append(texts_node)
        
        texts_items = [
            (_('Constitution'), '/constitution/', 51),
            (_('Lois'), '/lois/', 52),
            (_('Décrets'), '/decrets/', 53),
            (_('Arrêtés'), '/arretes/', 54),
            (_('Circulaires'), '/circulaires/', 55),
            (_('Codes et règlements'), '/codes/', 56),
            (_('Documents de stratégie'), '/strategies/', 57),
        ]
        
        for title, url, node_id in texts_items:
            nodes.append(NavigationNode(
                title,
                url,
                node_id,
                4,  # parent_id
            ))
        
        # 5. Services en ligne
        services_node = NavigationNode(
            _('Services en ligne'),
            '#',
            5,
            attr={'icon': 'bi-globe2'}
        )
        nodes.append(services_node)
        
        services_items = [
            (_('Espace professionnel'), '/espace-pro/', 61),
            (_('Démarches administratives'), '/demarches/', 62),
            (_('Formulaires en ligne'), '/formulaires/', 63),
            (_('Demande de documents'), '/demande-documents/', 64),
            (_('Paiement en ligne'), '/paiement/', 65),
            (_('Suivi des dossiers'), '/suivi/', 66),
        ]
        
        for title, url, node_id in services_items:
            nodes.append(NavigationNode(
                title,
                url,
                node_id,
                5,  # parent_id
            ))
        
        # 6. Contact
        nodes.append(NavigationNode(
            _('Contact'),
            '/contact/',
            6,
            attr={'icon': 'bi-envelope'}
        ))
        
        return nodes

menu_pool.register_menu(MegaMenu)