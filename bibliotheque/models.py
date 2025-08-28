from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    date_naissance = models.DateField()

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    date_sortie = models.DateField()
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE, related_name='livres')

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['titre']


class Categorie(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['nom']


class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date']


class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f'Commentaire de {self.nom} sur {self.article.titre}'

    class Meta:
        ordering = ['date']


class Note(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['-date_modification']


class Feedback(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['-date_creation']
