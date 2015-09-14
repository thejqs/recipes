#!usr/bin/env python
from __future__ import division
from collections import OrderedDict


# runs the Ingredient model methods to scale a recipe.
# and yes, unit shifter is a Nirvana reference --
# deal with it. https://www.youtube.com/watch?v=zagAeZ5eH94
def unit_shifter(recipe, new_serving_size):

    scaled_units = []

    for ingredient in recipe.ingredients.all():
        if ingredient.quantity > 0:

            units_per_serving, conversion_dict = ingredient.units_per_serving
            cooking_units = ingredient.real_units(new_serving_size, units_per_serving, conversion_dict)
            scaled_units.append(cooking_units)

        else:
            raise Exception("Although zero or negative ingredient quantities are a charmingly metaphysical idea, we don't accept them.")

    return scaled_units
