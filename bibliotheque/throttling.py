from rest_framework.throttling import UserRateThrottle


class FeedbackCreateThrottle(UserRateThrottle):
    """
    Throttle limitant la création de feedbacks à 20 par jour par utilisateur
    """
    scope = 'feedback_create'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

    def allow_request(self, request, view):
        """
        N'appliquer le throttling qu'aux actions de création
        """
        if view.action != 'create':
            return True
        
        return super().allow_request(request, view)