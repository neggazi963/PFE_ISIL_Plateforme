from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    """Vue de la page d'accueil"""
    context = {
        # Statistiques statiques pour le moment
        'corpus_count': 32,
        'tools_count': 28,
        'projects_count': 45,
        'members_count': 1250,
        
        # Données factices pour le développement
        'news': [],
        'popular_resources': [],
        'upcoming_events': [],
        'new_members': [],
        'recent_discussions': [],
    }
    
    return render(request, 'core/home.html', context)



def about(request):
    """Vue de la page À propos"""
    return render(request, 'core/about.html')

def contact(request):
    """Vue de la page Contact"""
    if request.method == 'POST':
        # TODO: Implémenter la logique de traitement du formulaire
        pass
    return render(request, 'core/contact.html')

def terms(request):
    """Vue des conditions d'utilisation"""
    return render(request, 'core/terms.html')

def privacy(request):
    """Vue de la politique de confidentialité"""
    return render(request, 'core/privacy.html')
