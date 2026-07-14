from rest_framework import viewsets

from carsdb.models import parts
from carsdb.serializers import PartSerializer


class PartViewSet(viewsets.ModelViewSet):
    """
    CRUD API for parts.

    - GET list/detail: available without login
    - POST/PUT/PATCH/DELETE: require login + Django model permissions
      (add_parts / change_parts / delete_parts)
    """

    queryset = parts.objects.select_related('author').all()
    serializer_class = PartSerializer
    search_fields = ('type', 'model_p', 'params', 'author__username')
    ordering_fields = ('type', 'model_p', 'price', 'count_p', 'id')
    ordering = ('type', 'model_p')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
