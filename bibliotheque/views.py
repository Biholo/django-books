from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Auteur, Livre
from .serializers import AuteurSerializer, LivreSerializer


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
