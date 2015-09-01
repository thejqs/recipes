from django.db import models
from django.contrib.auth.models import User
from markupfield.fields import MarkupField


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

    def __unicode__(self):
        return '{} {} {}'.format(self.quantity, self.unit, self.name)


class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey('main.Recipe')

    def __unicode__(self):
        return '{} - {}'.format(self.recipe, self.created)

    class Meta:
        ordering = ['-created']
