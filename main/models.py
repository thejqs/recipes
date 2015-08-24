from django.db import models
from django.contrib.auth.models import User


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
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Hard'),
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
    instructions = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
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
        (1, 'Teaspoon'),
        (2, 'Dessert Spoon'),
        (3, 'Table Spoon'),
        (4, 'Fluid Ounce'),
        (5, 'Cup'),
        (6, 'Pint'),
        (7, 'Quart'),
        (8, 'Gallon'),
        (9, 'pinch'),
        (10, 'dash'),
    )

    name = models.CharField(max_length=255)
    unit = models.IntegerField(choices=UNIT_CHOICES)
    quantity = models.FloatField()

    def __unicode__(self):
        return '{} {} {}'.format(self.quantity, self.unit, self.name)


class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey('main.Recipe')

    def __unicode__(self):
        return '{} - {}'.format(self.recipe, self.created)
