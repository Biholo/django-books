from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Auteur, Livre, Article, Categorie, Commentaire
from .serializers import AuteurSerializer, LivreSerializer
from .forms import CommentaireForm, ArticleForm


class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer

    def get_queryset(self):
        queryset = Livre.objects.all()
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(titre__icontains=search)
        return queryset


class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer

    def get_queryset(self):
        queryset = Auteur.objects.all()
        year = self.request.query_params.get('year')
        if year is not None:
            queryset = queryset.filter(date_naissance__year__gt=int(year))
        return queryset

    @action(detail=True, methods=['get'])
    def titres(self, request, pk=None):
        auteur = self.get_object()
        titres = auteur.livres.values_list('titre', flat=True)
        return Response({'titres': list(titres)})


# Vues Django traditionnelles (MVT)
def home(request):
    """Page d'accueil avec statistiques"""
    context = {
        'total_auteurs': Auteur.objects.count(),
        'total_livres': Livre.objects.count(),
        'total_categories': Categorie.objects.count(),
        'total_articles': Article.objects.count(),
        'total_commentaires': Commentaire.objects.count(),
    }
    return render(request, 'bibliotheque/home.html', context)


def current_datetime(request):
    """Vue fonction qui affiche la date et heure courantes"""
    now = datetime.now()
    html = f"<html><body><h1>Il est actuellement {now.strftime('%d/%m/%Y %H:%M:%S')}</h1></body></html>"
    return HttpResponse(html)


class ArticleListView(ListView):
    model = Article
    template_name = 'bibliotheque/article_list.html'
    context_object_name = 'articles'
    paginate_by = 5
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categorie.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'bibliotheque/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentaires'] = self.object.commentaires.filter(actif=True)
        context['comment_form'] = CommentaireForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = self.object
            commentaire.save()
            messages.success(request, 'Votre commentaire a été ajouté avec succès !')
            return redirect('article-detail', pk=self.object.pk)
        else:
            messages.error(request, 'Erreur dans le formulaire de commentaire.')
            return self.get(request, *args, **kwargs)


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'bibliotheque/article_form.html'
    success_url = reverse_lazy('article-list')

    def form_valid(self, form):
        messages.success(self.request, 'Article créé avec succès !')
        return super().form_valid(form)
