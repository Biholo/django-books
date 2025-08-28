from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui autorise l'édition/suppression d'un objet
    uniquement si obj.owner == request.user
    """

    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissions d'écriture seulement pour le propriétaire
        return obj.owner == request.user


def IsInGroup(group_name):
    """
    Factory fonction qui retourne une permission personnalisée qui vérifie l'appartenance à un groupe
    """
    
    class GroupPermission(permissions.BasePermission):
        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False
            
            return request.user.groups.filter(name=group_name).exists()
    
    return GroupPermission


class IsFeedbackOwnerOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Permission pour les feedbacks :
    - Tous peuvent lire
    - Propriétaire peut créer/modifier/voir les siens
    - Modérateurs peuvent supprimer tous les feedbacks
    """

    def has_permission(self, request, view):
        # Lecture autorisée à tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Écriture nécessite une authentification
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Lecture autorisée à tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Suppression autorisée aux modérateurs
        if request.method == 'DELETE':
            return (request.user and request.user.is_authenticated and 
                   request.user.groups.filter(name='moderator').exists())
        
        # Modification autorisée au propriétaire
        return obj.owner == request.user