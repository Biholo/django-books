from django.contrib import admin
from .models import Auteur, Livre, Categorie, Article, Commentaire


@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'date_naissance', 'nombre_livres']
    list_filter = ['date_naissance']
    search_fields = ['nom']
    ordering = ['nom']

    def nombre_livres(self, obj):
        return obj.livres.count()
    nombre_livres.short_description = 'Nombre de livres'


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'date_sortie']
    list_filter = ['date_sortie', 'auteur']
    search_fields = ['titre', 'auteur__nom']
    ordering = ['titre']
    date_hierarchy = 'date_sortie'


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'nombre_articles']
    search_fields = ['nom']
    ordering = ['nom']

    def nombre_articles(self, obj):
        return obj.articles.count()
    nombre_articles.short_description = 'Nombre d\'articles'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'date']
    list_filter = ['date', 'categorie']
    search_fields = ['titre', 'contenu']
    ordering = ['-date']
    date_hierarchy = 'date'


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ['nom', 'article', 'date', 'actif']
    list_filter = ['date', 'actif', 'article']
    search_fields = ['nom', 'email', 'contenu']
    list_editable = ['actif']
    ordering = ['-date']
