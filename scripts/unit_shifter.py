#!usr/bin/env python
from __future__ import division
from collections import OrderedDict


class UnitShifter():

    conversion_dict_tsp = OrderedDict([
        ('teaspoon', 1),
        ('tablespoon', 3),
        ('cup', 48),
        ('pint', 96),
        ('quart', 192),
        ('gallon', 768)
    ])

    conversion_dict_oz = OrderedDict([
                                        ('ounce', 1),
                                        ('pound', 16),
                                    ])

    def set_conversion_dict(self, recipe, conversion_dict_oz, conversion_dict_tsp):

        for ingredient in recipe.ingredients.all():
            if ingredient.quantity > 0:
                if ingredient.unit_string != 'ounce' or ingredient.unit_string != 'pound':
                    base_units = UnitShifter().by_volume(recipe, conversion_dict_tsp)
                    scaled_units = UnitShifter().scaled_volume(total_tsp)
                    return base units, scaled_units
                else:
                    base_units = UnitShifter().by_weight(recipe, conversion_dict_oz)
                    scaled_units = UnitShifter().scaled_weight(total_oz)
                    return base units, scaled_units
            else:
                return "Although zero or negative ingredient quantities are a charming idea, we don't accept them."

    def by_weight(self, recipe, conversion_dict_oz):

        # new_serving_size = USER INPUT

        for ingredient in recipe.ingredients.all():

                base_unit = conversion_dict_oz[ingredient.unit_string] * ingredient.quantity

                unit_per_serving = (base_unit / recipe.servings)

                total_oz = (new_serving_size * unit_per_serving)

                return total_oz

    def by_volume(self, recipe, conversion_dict_tsp):

        # new_serving_size = USER INPUT

        for ingredient in recipe.ingredients.all():

            base_unit = conversion_dict_tsp[ingredient.unit_string] * ingredient.quantity

            unit_per_serving = (base_unit / recipe.servings)

            total_tsp = (new_serving_size * unit_per_serving)

            return total_tsp

    def scaled_volume(self, total_tsp):

        ingr = []

        for k, conversion_factor in reversed(self.conversion_dict_tsp.items()):
            remainder = total_tsp % conversion_factor
            if total_tsp >= conversion_factor:
                converted_units = int(total_tsp // conversion_factor)
                ingr.append((k, converted_units))

                if remainder != 0:
                    total_tsp = remainder
                else:
                    break

            # print total_tsp, k, self.conversion_dict_tsp.keys()[0]
            if total_tsp < 1 and k == self.conversion_dict_tsp.keys()[0]:
                if ingr and ingr[-1][0] == self.conversion_dict_tsp.keys()[0]:
                    old_tuple = ingr[-1]
                    new_tuple = (old_tuple[0], old_tuple[1] + total_tsp)
                    ingr[-1] = new_tuple
                else:
                    ingr.append((k, total_tsp))

        return ingr

    def scaled_weight(self, total_oz):

        ingr = []

        for k, conversion_factor in reversed(self.conversion_dict_oz.items()):
            remainder = total_oz % conversion_factor
            if total_oz >= conversion_factor:
                converted_units = int(total_oz // conversion_factor)
                ingr.append((k, converted_units))

                if remainder != 0:
                    total_oz = remainder
                else:
                    break

            # print total_tsp, k, self.conversion_dict_tsp.keys()[0]
            if total_oz < 1 and k == self.conversion_dict_oz.keys()[0]:
                if ingr and ingr[-1][0] == self.conversion_dict_oz.keys()[0]:
                    old_tuple = ingr[-1]
                    new_tuple = (old_tuple[0], old_tuple[1] + total_oz)
                    ingr[-1] = new_tuple
                else:
                    ingr.append((k, total_oz))

        return ingr
