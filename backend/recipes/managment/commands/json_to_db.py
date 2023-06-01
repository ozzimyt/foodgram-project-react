import json

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт из json в БД'

    def handle(self, *args, **kwargs):
        with open('data/ingredients.json', 'r', encoding='utf-8') as _:
            data = json.load(_)

        for row in data:
            account = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            account.save()
