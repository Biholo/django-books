from rest_framework import serializers
from .models import Auteur, Livre, Article, Categorie, Commentaire, Note, Feedback


class LivreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = ['id', 'titre', 'date_sortie', 'auteur']


class AuteurSerializer(serializers.ModelSerializer):
    livres = LivreSerializer(many=True, read_only=True)

    class Meta:
        model = Auteur
        fields = ['id', 'nom', 'date_naissance', 'livres']


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom']


class ArticleSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'titre', 'contenu', 'date', 'categorie']


class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ['id', 'nom', 'email', 'contenu', 'date', 'actif']


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'titre', 'contenu', 'owner', 'date_creation', 'date_modification']


class CommentViewSerializer(serializers.ModelSerializer):
    article_titre = serializers.CharField(source='article.titre', read_only=True)
    
    class Meta:
        model = Commentaire
        fields = ['id', 'nom', 'email', 'contenu', 'date', 'actif', 'article', 'article_titre']


class FeedbackSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['id', 'titre', 'contenu', 'owner', 'date_creation']
