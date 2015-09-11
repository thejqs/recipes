from __future__ import division
from django.db import models
from django.contrib.auth.models import User
from markupfield.fields import MarkupField
from collections import OrderedDict


class Recipe(models.Model):

    RATING_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    DIFFICULTY_CHOICES = (
        (0, ''),
        (1, 'Simple'),
        (2, 'Intermediate'),
        (3, 'Challenging'),
    )

    MEAL_CHOICES = (
        (0, ''),
        (1, 'Breakfast'),
        (2, 'Lunch'),
        (3, 'Dinner'),
        (4, 'Snack'),
        (5, 'Dessert'),
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    instructions = MarkupField(markup_type='markdown', null=True, blank=True)
    notes = MarkupField(markup_type='markdown', null=True, blank=True)
    source = models.TextField(null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=0)
    meal = models.IntegerField(choices=MEAL_CHOICES, default=0)
    servings = models.IntegerField()
    exclude_from_search = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Ingredient(models.Model):

    UNIT_CHOICES = (
        ('', 'Unit Type'),
        (1, 'teaspoon'),
        (2, 'tablespoon'),
        (3, 'ounce'),
        (4, 'cup'),
        (5, 'pint'),
        (6, 'quart'),
        (7, 'pound'),
        (8, 'gallon'),
        (9, 'pinch'),
        (10, 'dash'),
    )

    name = models.CharField(max_length=255)
    unit = models.IntegerField(choices=UNIT_CHOICES)
    quantity = models.FloatField()
    recipe = models.ForeignKey('Recipe', related_name='ingredients')

    @property
    def unit_string(self):
        for unit in Ingredient.UNIT_CHOICES:
            if unit[0] == self.unit:
                return unit[1]

        return ''

    @property
    def units_per_serving(self):
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

        units_per_serving = 0
        conversion_dict = {}

        if self.unit_string != 'ounce' or self.unit_string != 'pound':
            conversion_dict = conversion_dict_tsp
            units_per_serving = (self.quantity * conversion_dict[self.unit_string]) / recipe.servings

        else:
            conversion_dict = conversion_dict_oz
            units_per_serving = (self.quantity * conversion_dict[self.unit_string]) / recipe.servings

        return units_per_serving, conversion_dict

    def real_units(self, new_serving_size, units_per_serving, conversion_dict):
        ingr = []
        total_units = units_per_serving * new_serving_size

        for k, conversion_factor in reversed(self.conversion_dict.items()):
            remainder = total_units % conversion_factor
            if total_units >= conversion_factor:
                converted_units = int(total_units // conversion_factor)
                ingr.append((k, converted_units))

                if remainder != 0:
                    total_units = remainder
                else:
                    break

            if total_units < 1 and k == self.conversion_dict.keys()[0]:
                if ingr and ingr[-1][0] == self.conversion_dict.keys()[0]:
                    old_tuple = ingr[-1]
                    new_tuple = (old_tuple[0], old_tuple[1] + total_units)
                    ingr[-1] = new_tuple
                else:
                    ingr.append((k, total_units))

        return ingr

    def __unicode__(self):
        return '{} {} {}'.format(self.quantity, self.unit, self.name)


class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey('main.Recipe')

    def __unicode__(self):
        return '{} - {}'.format(self.recipe, self.created)

    class Meta:
        ordering = ['-created']
