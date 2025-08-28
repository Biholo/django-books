from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from .models import Feedback, Note, Commentaire, Article, Categorie
from datetime import datetime, timedelta
from django.utils import timezone


class FeedbackAPITestCase(TestCase):
    def setUp(self):
        # Créer les utilisateurs
        self.user1 = User.objects.create_user(
            username='user1',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            password='password123'
        )
        self.moderator = User.objects.create_user(
            username='moderator',
            password='password123'
        )
        
        # Créer le groupe modérateur
        self.moderator_group = Group.objects.create(name='moderator')
        self.moderator.groups.add(self.moderator_group)
        
        # Créer les tokens
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.token_moderator = Token.objects.create(user=self.moderator)
        
        # Créer le client API
        self.client = APIClient()
        
        # Créer des feedbacks de test
        self.feedback1 = Feedback.objects.create(
            titre="Feedback User1",
            contenu="Contenu du feedback 1",
            owner=self.user1
        )
        self.feedback2 = Feedback.objects.create(
            titre="Feedback User2", 
            contenu="Contenu du feedback 2",
            owner=self.user2
        )

    def test_anonymous_can_read_feedbacks(self):
        """Test que les anonymes peuvent lire les feedbacks"""
        response = self.client.get('/api/feedbacks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_anonymous_cannot_create_feedback(self):
        """Test que les anonymes ne peuvent pas créer de feedback"""
        data = {
            'titre': 'Test Anonymous',
            'contenu': 'Contenu test'
        }
        response = self.client.post('/api/feedbacks/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_can_create_feedback(self):
        """Test qu'un utilisateur connecté peut créer un feedback"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        data = {
            'titre': 'Nouveau feedback',
            'contenu': 'Contenu du nouveau feedback'
        }
        response = self.client.post('/api/feedbacks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], str(self.user1))

    def test_owner_can_edit_own_feedback(self):
        """Test que le propriétaire peut modifier son feedback"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        data = {
            'titre': 'Feedback modifié',
            'contenu': 'Contenu modifié'
        }
        response = self.client.put(f'/api/feedbacks/{self.feedback1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titre'], 'Feedback modifié')

    def test_user_cannot_edit_others_feedback(self):
        """Test qu'un utilisateur ne peut pas modifier le feedback d'un autre"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        data = {
            'titre': 'Tentative de modification',
            'contenu': 'Contenu modifié'
        }
        response = self.client.put(f'/api/feedbacks/{self.feedback2.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_feedback(self):
        """Test qu'un utilisateur normal ne peut pas supprimer de feedback"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.delete(f'/api/feedbacks/{self.feedback1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_delete_any_feedback(self):
        """Test qu'un modérateur peut supprimer n'importe quel feedback"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_moderator.key)
        response = self.client.delete(f'/api/feedbacks/{self.feedback1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Vérifier que le feedback a été supprimé
        self.assertFalse(Feedback.objects.filter(id=self.feedback1.id).exists())

    def test_throttling_feedback_creation(self):
        """Test du throttling pour la création de feedbacks (limité à 20 par jour)"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        
        # Créer 20 feedbacks (max autorisé)
        for i in range(20):
            data = {
                'titre': f'Feedback {i}',
                'contenu': f'Contenu {i}'
            }
            response = self.client.post('/api/feedbacks/', data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Le 21ème devrait être refusé
        data = {
            'titre': 'Feedback en trop',
            'contenu': 'Ce feedback devrait être refusé'
        }
        response = self.client.post('/api/feedbacks/', data)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class PermissionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.admin = User.objects.create_user(
            username='admin',
            password='password123',
            is_staff=True
        )
        self.moderator = User.objects.create_user(
            username='moderator',
            password='password123'
        )
        
        # Créer le groupe modérateur
        moderator_group = Group.objects.create(name='moderator')
        self.moderator.groups.add(moderator_group)
        
        self.token_user = Token.objects.create(user=self.user)
        self.token_admin = Token.objects.create(user=self.admin)
        self.token_moderator = Token.objects.create(user=self.moderator)
        
        self.client = APIClient()
        
        # Créer des données de test
        self.note = Note.objects.create(
            titre="Note de test",
            contenu="Contenu de la note",
            owner=self.user
        )
        
        self.categorie = Categorie.objects.create(nom="Test")
        self.article = Article.objects.create(
            titre="Article test",
            contenu="Contenu article",
            categorie=self.categorie
        )
        self.commentaire = Commentaire.objects.create(
            nom="Commentateur",
            email="test@test.com",
            contenu="Commentaire test",
            article=self.article
        )

    def test_articles_public_access(self):
        """Test que les articles sont publics (AllowAny)"""
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_livres_read_only_for_anonymous(self):
        """Test que les livres sont en lecture seule pour les anonymes"""
        # Lecture OK
        response = self.client.get('/api/livres/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Création refusée
        data = {'titre': 'Livre test', 'date_sortie': '2023-01-01', 'auteur': 1}
        response = self.client.post('/api/livres/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_required_by_default(self):
        """Test que les auteurs nécessitent d'être admin (permission globale)"""
        # Utilisateur normal refusé
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user.key)
        response = self.client.get('/api/auteurs/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin autorisé
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)
        response = self.client.get('/api/auteurs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_note_owner_permission(self):
        """Test des permissions IsOwnerOrReadOnly pour les notes"""
        # Le propriétaire peut modifier
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user.key)
        data = {
            'titre': 'Note modifiée',
            'contenu': 'Contenu modifié'
        }
        response = self.client.put(f'/api/notes/{self.note.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_can_delete_comments(self):
        """Test qu'un modérateur peut supprimer des commentaires"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_moderator.key)
        response = self.client.delete(f'/api/comments/{self.commentaire.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_regular_user_cannot_delete_comments(self):
        """Test qu'un utilisateur normal ne peut pas supprimer de commentaires"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user.key)
        response = self.client.delete(f'/api/comments/{self.commentaire.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
