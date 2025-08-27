from django import forms
from .models import Commentaire, Article


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['nom', 'email', 'contenu']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'placeholder': 'votre@email.com'}),
            'contenu': forms.Textarea(attrs={
                'placeholder': 'Votre commentaire...',
                'rows': 4
            }),
        }


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'categorie']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de l\'article'}),
            'contenu': forms.Textarea(attrs={
                'placeholder': 'Contenu de l\'article...',
                'rows': 10
            }),
        }
