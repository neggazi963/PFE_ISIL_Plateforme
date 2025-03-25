from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from news.models import News
from events.models import Event
from resources.models import Resource
from community.models import Discussion, Profile
from corpus.models import Corpus
from tools.models import Tool
from projects.models import Project

def home(request):
    """Vue de la page d'accueil"""
    context = {
        # Statistiques
        'corpus_count': Corpus.objects.count(),
        'tools_count': Tool.objects.count(),
        'projects_count': Project.objects.filter(status='active').count(),
        'members_count': Profile.objects.count(),
        
        # Actualités récentes
        'news': News.objects.order_by('-date')[:3],
        
        # Ressources populaires
        'popular_resources': Resource.objects.order_by('-views')[:3],
        
        # Événements à venir
        'upcoming_events': Event.objects.filter(
            status='upcoming'
        ).order_by('date')[:3],
        
        # Nouveaux membres
        'new_members': Profile.objects.order_by('-date_joined')[:3],
        
        # Discussions récentes
        'recent_discussions': Discussion.objects.order_by('-last_activity')[:2],
    }
    
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    """Vue du tableau de bord utilisateur"""
    user = request.user
    context = {
        'my_corpus': Corpus.objects.filter(author=user)[:5],
        'my_tools': Tool.objects.filter(author=user)[:5],
        'my_projects': Project.objects.filter(members=user)[:5],
        'my_discussions': Discussion.objects.filter(participants=user)[:5],
        'bookmarked_resources': Resource.objects.filter(bookmarks=user)[:5],
    }
    
    return render(request, 'dashboard.html', context)

def about(request):
    """Vue de la page À propos"""
    return render(request, 'about.html')

def contact(request):
    """Vue de la page Contact"""
    return render(request, 'contact.html')

def terms(request):
    """Vue des conditions d'utilisation"""
    return render(request, 'terms.html')

def privacy(request):
    """Vue de la politique de confidentialité"""
    return render(request, 'privacy.html')
