from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Auteur, Livre, Article, Categorie, Commentaire, Note, Feedback
from .serializers import AuteurSerializer, LivreSerializer, ArticleSerializer, NoteSerializer, CommentViewSerializer, FeedbackSerializer
from .permissions import IsOwnerOrReadOnly, IsInGroup, IsFeedbackOwnerOrModeratorOrReadOnly
from .throttling import FeedbackCreateThrottle
from .forms import CommentaireForm, ArticleForm


class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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


class ArticleListViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentViewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """
        Les modérateurs peuvent supprimer, les autres seulement lire/créer/modifier
        """
        if self.action == 'destroy':
            permission_classes = [IsInGroup('moderator')]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        
        return [permission() for permission in permission_classes]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsFeedbackOwnerOrModeratorOrReadOnly]
    throttle_classes = [FeedbackCreateThrottle]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Les utilisateurs voient tous les feedbacks (lecture publique)
        mais ne peuvent modifier que les leurs
        """
        return Feedback.objects.all()


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
