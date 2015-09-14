from django.test import TestCase
from django.contrib.auth.models import User
from scripts.unit_shifter import UnitShifter
from main.models import Recipe, Ingredient

# Create your tests here.


class ShiftingUnitsTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            username='admin'
        )

        Recipe.objects.create(
            creator=User.objects.get(username='admin'),
            name="pig \'n\' stuff",
            instructions="If one of the ingredients is soap, please ignore. Please.",
            rating=3,
            difficulty=2,
            meal=2,
            servings=3,
        )

        Ingredient.objects.create(
            name="pineapple juice",
            unit=4, # cups
            quantity=3, # 144 tsp
            recipe=Recipe.objects.get(servings=3)
        )

        Ingredient.objects.create(
            name="thunder stalks",
            unit=5, # tbsp
            quantity=2.5, # 240 tsp
            recipe=Recipe.objects.get(servings=3)
        )

        Ingredient.objects.create(
            name="monkey tears",
            unit=2, # tbsp
            quantity=-2, # -6 tsp
            recipe=Recipe.objects.get(servings=3)
        )

        Ingredient.objects.create(
            name="pork butt",
            unit=7, # pounds
            quantity=6, # 96 oz
            recipe=Recipe.objects.get(servings=3)
        )

        Ingredient.objects.create(
            name="onion",
            unit=4, # cups
            quantity=.6, # 48 tsp
            recipe=Recipe.objects.get(servings=3)
        )

        Ingredient.objects.create(
            name="Spam",
            unit=7, # pounds
            quantity=.3, # 96 oz
            recipe=Recipe.objects.get(servings=3)
        )

    def test_disallow_negatives(self):
        """Nothing runs if ingredient quantity is negative"""
        recipe = Recipe.objects.first()
        u_s = UnitShifter()
        try:
            u_s.scale_recipe(recipe, -3)
            assert False
        except:
            assert True

        print "Good job. A recipe with a new positive serving size."

    def test_conversion_dict_oz(self):
        """The script chooses the correction conversion_dict for weight"""
        recipe = Recipe.objects.get(rating=3)
        ingredient = recipe.ingredients.get(name="pork butt")
        choose_dict = UnitShifter().set_conversion_dict(ingredient)
        self.assertEqual(choose_dict.get('pound'), 16)

        print "This thing can tell weight from volume."

    def test_conversion_dict_tsp(self):
        """The script chooses the correction conversion_dict for volume"""
        recipe = Recipe.objects.get(rating=3)
        ingredient = recipe.ingredients.get(name="pineapple juice")
        choose_dict = UnitShifter().set_conversion_dict(ingredient)
        self.assertEqual(choose_dict.get('cup'), 48)

        print "This thing can tell volume from weight."

    def test_method_conversion_dict_oz(self):
        """The script applies the oz conversion_dict to the by_weight method"""
        recipe = Recipe.objects.get(rating=3)
        new_serving_size = 8
        ingredient = recipe.ingredients.get(name="pork butt")
        weight = UnitShifter().set_conversion_dict(ingredient)

        total_oz = UnitShifter().by_weight(recipe, ingredient, new_serving_size, weight)

        self.assertEqual(total_oz, 256)

        print "Holy crap. The oz dictionary to the right place."

    def test_method_conversion_dict_tsp(self):
        """The script applies the tsp conversion_dict to the by_volume method"""
        recipe = Recipe.objects.get(rating=3)
        new_serving_size = 8
        ingredient = recipe.ingredients.get(name="pineapple juice")
        volume = UnitShifter().set_conversion_dict(ingredient)

        total_tsp = UnitShifter().by_volume(recipe, ingredient, new_serving_size, volume)

        self.assertEqual(total_tsp, 384)

        print "Holy crap. The tsp dictionary to the right place."

    def test_by_weight_less_than_one(self):
        """Method by_weight properly handles an ingredient quantity of < 1"""
        recipe = Recipe.objects.get(rating=3)
        new_serving_size = 8
        ingredient = recipe.ingredients.get(name="Spam")
        weight = UnitShifter().set_conversion_dict(ingredient)

        total_oz = UnitShifter().by_weight(recipe, ingredient, new_serving_size, weight)

        self.assertEqual(total_oz, .8)

        print "The by_weight method can handle < 1"

    def test_by_weight_low_integer(self):
        """Method by_weight handles a low integer properly"""
        recipe = Recipe.objects.get(rating=3)
        new_serving_size = 2
        ingredient = recipe.ingredients.get(name="pork butt")
        weight = UnitShifter().set_conversion_dict(ingredient)

        total_oz = UnitShifter().by_weight(recipe, ingredient, new_serving_size, weight)

        self.assertEqual(total_oz, 4)

        print "The by_weight method can handle a small int."

    def test_by_weight_high_integer(self):
        """Method by_weight handles a high integer properly"""
        recipe = Recipe.objects.get(rating=3)
        new_serving_size = 32478
        ingredient = recipe.ingredients.get(name="pork butt")
        weight = UnitShifter().set_conversion_dict(ingredient)

        total_oz = UnitShifter().by_weight(recipe, ingredient, new_serving_size, weight)

        self.assertEqual(total_oz, 64956)

        print "The by_weight method can handle a large int."

    # def test_by_weight_float(self):
    #     """Method by_weight properly handles a float"""

    def test_by_volume_less_than_one(self):
        """Method by_volume properly handles a quantity of < 1"""
        recipe = Recipe.objects.get(rating=3)
        new_serving_size = 4
        ingredient = recipe.ingredients.get(name="onion")
        volume = UnitShifter().set_conversion_dict(ingredient)

        total_tsp = UnitShifter().by_weight(recipe, ingredient, new_serving_size, volume)

        self.assertEqual(total_tsp, .8)

        print "The by_volume method can handle < 1"

    def test_by_volume_low_integer(self):
        """Method by_volume handles a low integer properly"""
        recipe = Recipe.objects.get(rating=3)
        new_serving_size = 2
        ingredient = recipe.ingredients.get(name="pineapple juice")
        volume = UnitShifter().set_conversion_dict(ingredient)

        total_tsp = UnitShifter().by_weight(recipe, ingredient, new_serving_size, volume)

        self.assertEqual(total_tsp, 2)

        print "The by_volume method can handle a small int."

    def test_by_volume_high_integer(self):
        """Method by_volume handles a high integer properly"""
        recipe = Recipe.objects.get(rating=3)
        new_serving_size = 1475822
        ingredient = recipe.ingredients.get(name="pineapple juice")
        volume = UnitShifter().set_conversion_dict(ingredient)

        total_tsp = UnitShifter().by_weight(recipe, ingredient, new_serving_size, volume)

        self.assertEqual(total_tsp, 1475822)

        print "The by_volume method can handle a large int."

    # def test_by_volume_float(self):
    #     """Method by_volume properly handles a float"""

    def test_ordered_dict_tuples(self):
        """Values in OrderedDict are associated correctly"""
        u_s = UnitShifter()

        self.assertEqual(u_s.conversion_dict_tsp[0][0], 'teaspoon')
        self.assertEqual(u_s.conversion_dict_tsp[0][1], 1)

        print "The tuple values in the OrderedDict are in the correct order"

    def test_ordered_dict_ordering(self):
        """Items in OrderedDict are ordered correctly"""
        u_s = UnitShifter()

        self.assertEqual(u_s.conversion_dict_tsp[0][0], 'teaspoon')
        self.assertEqual(u_s.conversion_dict_tsp[1][0], 'tablespoon')
        self.assertEqual(u_s.conversion_dict_tsp[5][0], 'gallon')

        print "The OrderedDict is ordered correctly."

    def test_scale_volume_less_than_one(self):
        """Method scaled_from_tsp properly handles a value < 1"""
        total_tsp = .5

        units = UnitShifter().scaled_from_tsp(total_tsp)

        self.assertEqual(units[0][0], 'teaspoon')
        self.assertEqual(units[0][1], .5)

    def test_scale_volume_small_integer(self):
        """Method scaled_from_tsp properly handles a small integer"""
        total_tsp = 18

        units = UnitShifter().scaled_from_tsp(total_tsp)

        self.assertEqual(units[0][0], 'tablespoon')
        self.assertEqual(units[0][1], 6)

    def test_scale_volume_large_integer(self):
        """Method scaled_from_tsp properly handles a large integer"""
        total_tsp = 14785290

        units = UnitShifter().scaled_from_tsp(total_tsp)

        self.assertEqual(units[0][0], 'gallon')
        self.assertEqual(units[0][1], 19251)
        self.assertEqual(units[1][0], 'quart')
        self.assertEqual(units[1][1], 2)
        self.assertEqual(units[2][0], 'pint')
        self.assertEqual(units[2][1], 2)
        self.assertEqual(units[3][0], 'tablespoon')
        self.assertEqual(units[3][1], 14)
        self.assertEqual(units[4][0], 'teaspoon')
        self.assertEqual(units[4][1], 1)

    # def test_scale_volume_float(self):
    #     """Method scale_volume properly handles a float"""

    def test_scale_weight_less_than_one(self):
        """Method scaled_from_oz properly handles a value < 1"""
        total_oz = .5

        units = UnitShifter().scaled_from_oz(total_oz)

        self.assertEqual(units[0][0], 'ounce')
        self.assertEqual(units[0][1], .5)

    def test_scale_weight_small_integer(self):
        """Method scaled_from_oz properly handles a small integer"""
        total_oz = 21

        units = UnitShifter().scaled_from_oz(total_oz)

        self.assertEqual(units[0][0], 'pound')
        self.assertEqual(units[0][1], 1)
        self.assertEqual(units[1][0], 'ounce')
        self.assertEqual(units[1][1], 5)

    def test_scale_weight_large_integer(self):
        """Method scaled_from_oz properly handles a large integer"""
        total_oz = 329072970129346507

        units = UnitShifter().scaled_from_oz(total_oz)

        self.assertEqual(units[0][0], 'pound')
        self.assertEqual(units[0][1], 20567060633084156)
        self.assertEqual(units[1][0], 'ounce')
        self.assertEqual(units[1][1], 11)

    # def test_scale_weight_float(self):
    #     """Method scale_weight properly handles a float"""
