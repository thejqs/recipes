#!usr/bin/env python
from __future__ import division
from collections import OrderedDict


class UnitShifter():
    def scale_recipe(self, recipe, new_serving_size):

        scaled_units = []

        for ingredient in recipe.ingredients.all():
            if ingredient.quantity > 0:
                total_units = ingredient.units_per_serving
                cooking_units = ingredient.real_units(units_per_serving, conversion_dict)
                scaled_units.append(cooking_units)

        return scaled_units
