from django_filters import rest_framework as filters
from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    """Фильтр Title по имени, полю slug жанра и категории."""
    genre = filters.CharFilter(lookup_expr='slug')
    category = filters.CharFilter(lookup_expr='slug')
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')
