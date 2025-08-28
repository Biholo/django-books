from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LivreViewSet, AuteurViewSet, ArticleListViewSet, NoteViewSet, CommentViewSet, FeedbackViewSet,
    home, current_datetime, ArticleListView, ArticleDetailView, ArticleCreateView
)

router = DefaultRouter()
router.register(r'livres', LivreViewSet)
router.register(r'auteurs', AuteurViewSet)
router.register(r'articles', ArticleListViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'feedbacks', FeedbackViewSet)

urlpatterns = [
    # API REST (DRF)
    path('api/', include(router.urls)),
    
    # Vues web traditionnelles (MVT)
    path('', home, name='home'),
    path('now/', current_datetime, name='current-datetime'),
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/nouveau/', ArticleCreateView.as_view(), name='article-create'),
]
