import csv

from backend.api.models import Ingredient, Unit


def create_units(ingedients_list):
    unit_set = set()
    for unit in ingedients_list:
        unit_set.add(unit[1])
    for unit in unit_set:
        Unit.objects.create(name=unit)

def create_ingredients(ingedients_list):
    ingredients_to_create = []
    for row in list(ingedients_list):
        unit = Unit.objects.get(name=row[1])
        ingredients_to_create.append(
            Ingredient(name=row[0], measurement_unit=unit)
        )
    Ingredient.objects.bulk_create(ingredients_to_create)


csv_path = "../data/ingredients.csv"
with open(csv_path, "r") as ingredients_file:
    ingedients_list = csv.reader(ingredients_file)
    create_units(ingedients_list)

with open(csv_path, "r") as ingredients_file:
    ingedients_list = csv.reader(ingredients_file)
    create_ingredients(ingedients_list)