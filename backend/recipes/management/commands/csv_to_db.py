import os.path as path
from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


FILE_DIR = path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Импорт из CSV в БД'

    def handle(self, *args, **options):
        self.stdout.write('попытка импорта ингридиентов.')
        try:
            with open(
                path.join(FILE_DIR, 'ingredients.csv'),
                'r',
                encoding='utf-8'
            ) as file:
                for name, measurement_unit in DictReader(file):
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                self.stdout.write(
                    f'Импрот ингридиентов из "{file.name}" завершен.')
        except FileNotFoundError:
            self.stdout.write(
                f'фаил "{file.name}" с ингридиентами не найден !')
        except Exception as e:
            self.stdout.write(
                f'ошибка при импорте из файла "{file.name}" :', e)

        self.stdout.write('попытка импорта тегов.')
        try:
            with open(
                path.join(FILE_DIR, 'tags.csv'),
                'r',
                encoding='utf-8'
            ) as file:
                for name, color, slug in DictReader(file):
                    Tag.objects.get_or_create(
                        name=name,
                        color=color,
                        slug=slug
                    )
                self.stdout.write(f'Импрот из тегов "{file.name}" завершен.')
        except FileNotFoundError:
            self.stdout.write(f'фаил "{file.name}" с тегами не найден !')
        except Exception as e:
            self.stdout.write(
                f'ошибка при импорте из файла "{file.name}" :', e)
