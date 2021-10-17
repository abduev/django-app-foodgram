import csv

from django.core.exceptions import ObjectDoesNotExist


def create_units(source):
    from api.models import Unit
    set_of_units = set()
    units = []
    for row in list(source):
        set_of_units.add(row[1])
    for unit in set_of_units:
        units.append(Unit(name=unit))
    Unit.objects.bulk_create(units)


def create_ingredients(source):
    from api.models import Ingredient, Unit
    ingredients = []
    for row in list(source):
        try:
            unit = Unit.objects.get(name=row[1])
        except ObjectDoesNotExist:
            print('Invalid measurement unit')
        ingredients.append(Ingredient(name=row[0], measurement_unit=unit))
    Ingredient.objects.bulk_create(ingredients)


csv_path = './data/ingredients.csv'
with open(csv_path, 'r') as fixtures_obj:
    source = csv.reader(fixtures_obj)
    create_units(source)


with open(csv_path, 'r') as fixtures_obj:
    source = csv.reader(fixtures_obj)
    create_ingredients(source)
