import csv

from django.conf import settings
from django.core.management import BaseCommand

from ._utils import loading
from ...models import (
    Category, Genre, Title, TitlesGenre, Review, User,
    Comment)

path = f'{settings.BASE_DIR}/static/data'


class Command(BaseCommand):
    help = 'Загрузка данных в БД из файлов csv'

    model_csv = {
        Category: 'category',
        Genre: 'genre',
        Title: 'titles',
        TitlesGenre: 'genre_title',
        User: 'users',
        Review: 'review',
        Comment: 'comments',
    }

    def handle(self, *args, **options):
        for model, file in self.model_csv.items():
            if model.objects.exists():
                raise Exception(f'Ошибка. Данные в модель {model.__name__}'
                      f'уже загружены.')
            else:
                print(f'Загрузка данных в модель {model.__name__}')
                for row in csv.DictReader(open(f'{path}/{file}.csv',
                                               encoding='utf-8')):
                    columns = loading(model, row)
                    columns.save()
                print(f'Данные в модель {model.__name__} загружены')
