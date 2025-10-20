from .models import Movie
import django_filters


class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.CharFilter(lookup_expr='icontains')
    director = django_filters.CharFilter(lookup_expr='icontains')
    release_date = django_filters.DateFilter(lookup_expr='exact')
    rating = django_filters.CharFilter(lookup_expr='exact') 
    rotten_tomatoes_rating = django_filters.CharFilter(lookup_expr='exact')
    actors = django_filters.CharFilter(lookup_expr='icontains')
    runtime = django_filters.CharFilter(lookup_expr='exact')
    awards = django_filters.CharFilter(lookup_expr='icontains')

    order_by = django_filters.OrderingFilter(
        choices=(
            ('title', 'Title (A-Z)'),
            ('-title', 'Title (Z-A)'),
            ('release_date', 'Release Date (Oldest first)'),
            ('-release_date', 'Release Date (Newest first)'),
            ('rating', 'IMDB Rating (Low to High)'),
            ('-rating', 'IMDB Rating (High to Low)'),
            ('rotten_tomatoes_rating', 'Rotten Tomatoes (Low to High)'),
            ('-rotten_tomatoes_rating', 'Rotten Tomatoes (High to Low)'),
            ('runtime', 'Runtime (Short to Long)'),
            ('-runtime', 'Runtime (Long to Short)'),
        ),
        fields={
            'title': 'title',
            'release_date': 'release_date',
            'rating': 'rating',
            'rotten_tomatoes_rating': 'rotten_tomatoes_rating',
            'runtime': 'runtime',
        }
    )

    class Meta:
        model = Movie
        paginate_by = 20 
        fields = ['title', 'genre', 'director', 'release_date', 'rating', 'rotten_tomatoes_rating',
                  'actors', 'runtime', 'awards'
        ]

