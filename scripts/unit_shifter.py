#!usr/bin/env python


class UnitShifter():

    conversion_dict = {
                            'teaspoon': 1,
                            'tablespoon': 3,
                            # 'eighth_cup': 6,
                            # 'sixth_cup': 8,
                            # 'quarter_cup': 12,
                            # 'third_cup': 16,
                            # 'half_cup': 24,
                            # 'two_thirds_cup': 32,
                            # 'three_quarters_cup': 36,
                            'cup': 48,
                            'pint': 96,
                            'quart': 192,
                            'gallon': 768
                        }

    ounces_to_pounds = {
                                        'ounce': 1,
                                        # 'quarter_pound': 4,
                                        # 'third_pound': 5.3333333
                                        # 'half_pound': 8,
                                        # 'two_thirds_pound': 10.6666667
                                        # 'three_quarters_pound': 12,
                                        'pound': 16
                                    }

    def to_tsp(self, recipe):
        change_in_serving = abs(new_serving_size - db_serving_size)

        for ingredient in recipe.ingredients.all():
            base_unit = conversion_dict[ingredient.unit] * ingredient.quantity

            unit_per_serving = base_unit / servings

            new_unit = (unit_per_serving * change_in_serving) + base_unit

            return new_unit, base_unit

    def scaled_units(self, new_unit, recipe):

        total_units = 0

        for k, v in conversion_dict.iteritems():
            if new_unit >= v:
                if new_unit % v == 0:
                    total_units += (new_unit / v)
                else:
                    new_unit / v
                    new_unit -= (new_unit * v)

            return total_units






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


