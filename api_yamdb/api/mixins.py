from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .permissions import (IsAdminOrReadOnly)


class CategoryGenreViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                           mixins.ListModelMixin, viewsets.GenericViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
