from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from .validators import get_year

message = ('Username содержит недопустимые символы {value}')


class UsernameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(
            RegexValidator(r'^[\w.@+-]+$', message)
        )


class User(AbstractUser):
    """Модель пользователя."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True, max_length=settings.EMAIL
    )
    username = UsernameField(
        verbose_name='Имя пользователя',
        help_text='Только буквы, цифры, @, +, -, _',
        max_length=settings.USERNAME,
        null=True,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=max((len(role[1]) for role in ROLES)),
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN or self.is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact='me'),
                name='username_is_not_me'
            )
        ]

    def __str__(self):
        return f'{self.username}({self.email})'


class Category_Genre_Model(models.Model):
    """Материнская модель для моделей Category и Genre."""

    name = models.CharField(verbose_name='Название',
                            max_length=settings.NAME)
    slug = models.SlugField(verbose_name='Слаг', unique=True,
                            max_length=settings.SLUG)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(Category_Genre_Model):
    """Категории произведений."""

    class Meta(Category_Genre_Model.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(Category_Genre_Model):
    """Жанры произведений."""

    class Meta(Category_Genre_Model.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения."""
    name = models.CharField(verbose_name='Название произведения',
                            max_length=settings.MAX_LEN)
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(get_year)],
        verbose_name='Год произведения', db_index=True)
    description = models.TextField(verbose_name='Описание', blank=True,
                                   null=True)
    genre = models.ManyToManyField(Genre, through='TitlesGenre',
                                   verbose_name='Жанр',
                                   blank=True,
                                   related_name='genre',
                                   help_text='Жанр произведения')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.SET_NULL, blank=True,
                                 null=True, related_name='category',
                                 help_text='Категория произведения')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitlesGenre(models.Model):
    """Реализация связи один ко многим произведений и жанров."""
    titles = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.titles} {self.genre}'


class ReviewAbstract(models.Model):
    """Материнская модель для моделей Review и Comment."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор',
        max_length=settings.MAX_LEN)
    text = models.TextField(verbose_name='Текст ревью',
                            max_length=settings.MAX_LEN)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Review(ReviewAbstract):
    """Отзывы на произведения. Отзыв привязан к определённому произведению."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='Произведение',
        max_length=settings.MAX_LEN
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[
            MaxValueValidator(10, 'Оценка не может быть больше 10'),
            MinValueValidator(1, 'Оценка не может быть меньше 1')
        ]
    )

    class Meta(ReviewAbstract.Meta):
        default_related_name = 'reviews'
        verbose_name = 'Ревью'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title'
            )
        ]


class Comment(ReviewAbstract):
    """Комментарии к отзывам. Комментарий привязан к определённому отзыву."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        max_length=settings.MAX_LEN,
        blank=True, null=True)

    class Meta(ReviewAbstract.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
