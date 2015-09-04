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

    def scale_recipe(self, recipe, new_serving_size):

        scaled_units = []

        for ingredient in recipe.ingredients.all():
            if ingredient.quantity > 0:
                get_dict = self.set_conversion_dict(ingredient)

                if get_dict == conversion_dict_tsp:
                    base_units = self.by_volume(ingredient, new_serving_size, conversion_dict_tsp)
                    scaled_units.append(self.scaled_volume(total_tsp))

                elif get_dict == conversion_dict_oz:
                    base_units = self.by_weight(ingredient, new_serving_size, conversion_dict_oz)
                    scaled_units = self.scaled_weight(total_oz)

                else:
                    raise Exception("Seriously, how does this not have weight or volume?")

            else:
                raise Exception("Although zero or negative ingredient quantities are a charmingly metaphysical idea, we don't accept them.")

        return scaled_units

    def set_conversion_dict(self, ingredient):

        # if ingredient.quantity > 0:
        if ingredient.unit_string != 'ounce' or ingredient.unit_string != 'pound':
            conversion_dict_tsp = self.conversion_dict_tsp
            return conversion_dict_tsp

        else:
            conversion_dict_oz = self.conversion_dict_oz
            return conversion_dict_oz

        # else:
            # return "Although zero or negative ingredient quantities are a charmingly metaphysical idea, we don't accept them."

    def by_weight(self, ingredient, new_serving_size, conversion_dict_oz):

        new_serving_size = abs(8)

        base_unit = conversion_dict_oz[ingredient.unit_string] * ingredient.quantity

        unit_per_serving = (base_unit / recipe.servings)

        total_oz = (new_serving_size * unit_per_serving)

        return total_oz

    def by_volume(self, ingredient, new_serving_size, conversion_dict_tsp):

        new_serving_size = abs(-8)

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
