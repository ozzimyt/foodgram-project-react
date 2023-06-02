import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Импорт из CSV в БД'

    def handle(self, *args, **options):
        files_path = ['./data/ingredients.csv', './data/tags.csv']
        for index, file_path in enumerate(files_path, start=1):
            try:
                with open(file_path, encoding='utf8') as file:
                    rows = list(csv.reader(file))
                    if index == 1:
                        objs = [Ingredient(*row) for row in rows]
                        Ingredient.objects.bulk_create(objs)
                    else:
                        objs = [Tag(*row) for row in rows]
                        Tag.objects.bulk_create(objs)
            except Exception as error:
                print('ошибка при импорте', error)
