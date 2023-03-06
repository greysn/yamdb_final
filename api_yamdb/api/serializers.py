from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User

from .validators import MixinValidatorUsername


class CategorySerializer(serializers.ModelSerializer):
    """Сериализер для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализер для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализер для модели Title для GET методов."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')
        read_only_fields = ('id', 'name', 'year', 'description',
                            'genre', 'category', 'rating')


class TitleCUDSerializer(serializers.ModelSerializer):
    """Сериализер для модели Title для CUD методов."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def to_representation(self, instance):
        return TitlesSerializer(instance).data

    def validate_year(self, value):
        current_year = timezone.now().year
        if not 0 <= value <= current_year:
            raise ValidationError('Проверьте год создания произведения.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализер для модели Review."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if Review.objects.filter(
                title=get_object_or_404(
                    Title,
                    pk=self.context['view'].kwargs.get('title_id')),
                    author=request.user
            ).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = ('id', 'author', 'score', 'text', 'pub_date', 'title')
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализер для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')


class UserSerializer(serializers.ModelSerializer, MixinValidatorUsername):
    """Сериалайзер для модели User."""

    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserEditSerializer(UserSerializer):
    """Сериалиазация модели User при get и patch запросах."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.Serializer, MixinValidatorUsername):
    """Сериализатор модели User, используемый при регистрации."""
    username = serializers.CharField(max_length=settings.USERNAME)
    email = serializers.EmailField()


class TokenSerializer(serializers.Serializer, MixinValidatorUsername):
    """"Проверка confirmation_code при регистрации."""
    username = serializers.CharField(max_length=settings.USERNAME)
    confirmation_code = serializers.CharField()
