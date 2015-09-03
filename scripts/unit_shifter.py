#!usr/bin/env python
from __future__ import division
from collections import OrderedDict


class UnitShifter():

    conversion_dict = OrderedDict([('teaspoon', 1), ('tablespoon', 3), ('cup', 48), ('pint', 96), ('quart', 192), ('gallon', 768)])

    ounces_to_pounds = {
                                        'ounce': 1,
                                        'pound': 16
                                    }

    def to_tsp(self, recipe):
        # change_in_serving = abs(new_serving_size - recipe.servings)

        for ingredient in recipe.ingredients.all():
            base_unit = conversion_dict[ingredient.unit_string] * ingredient.quantity

            unit_per_serving = base_unit / recipe.servings

            total_tsp = (new_serving_size * unit_per_serving)

            return total_tsp

    def scaled_units(self, total_tsp):

        ingr = []

        # total_units = 0

        for k, conversion_factor in reversed(self.conversion_dict.items()):
            # print k
            remainder = total_tsp % conversion_factor
            if total_tsp >= conversion_factor:
                converted_units = int(total_tsp // conversion_factor)
                ingr.append((k, converted_units))
                # import ipdb; ipdb.set_trace()

                if remainder != 0:
                    total_tsp = remainder

                else:
                    break

            print total_tsp, k, self.conversion_dict.keys()[0]
            if total_tsp < 1 and k == self.conversion_dict.keys()[0]:
                if ingr and ingr[-1][0] == self.conversion_dict.keys()[0]:
                    old_tuple = ingr[-1]
                    new_tuple = (old_tuple[0], old_tuple[1] + total_tsp)
                    ingr[-1] = new_tuple
                else:
                    ingr.append((k, total_tsp))

        return ingr


            #     total_units += (total_tsp / conversion_factor)

            # else:
            #     total_tsp / conversion_factor
            #     total_tsp -= (total_tsp * conversion_factor)

            #     return total_units






# if tsp < 3:
#     tsp

# if tsp >= 3:
#     tbsp = tsp * 3
#     if tbsp % 3 == 0:
#         tbsp
#     else:
#         tbsp + (tbsp % 3)

# if tbsp % 16 == 0:
#     cup = tbsp * 16


