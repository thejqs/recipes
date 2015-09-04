from django.test import TestCase
from main.scripts.unit_shifter import UnitShifter
from main.models import Recipe, Ingredient

# Create your tests here.


class ShiftingUnitsTestCase(TestCase):

    def setUp(self):
        Recipe.objects.create(
            creator=admin,
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
            quantity=3.2, # 153.6 tsp
        )

        Ingredient.objects.create(
            name="monkey tears",
            unit=2, # tbsp
            quantity=-2, # -6 tsp
        )

        Ingredient.objects.create(
            name="pork butt",
            unit=7, # pounds
            quantity=5.5, # 88 oz
        )

        Ingredient.objects.create(
            name="onion",
            unit=4, # cups
            quantity=1, # 48 tsp
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
        ingredient = Recipe.ingredients.get(name="pork butt")
        choose_dict = UnitShifter().set_conversion_dict(ingredient)
        self.assertEqual(choose_dict.get('pound'), 16)

        print "This thing can tell weight from volume."

    def test_conversion_dict_tsp(self):
        """The script chooses the correction conversion_dict for volume"""
        ingredient = Recipe.ingredients.get(name="pineapple juice")
        choose_dict = UnitShifter().set_conversion_dict()
        self.assertEqual(choose_dict.get('cup'), 48)

        print "This thing can tell volume from weight."

    def test_method_conversion_dict_oz(self):
        """The script applies the oz conversion_dict to the by_weight method"""
        new_serving_size = 8
        ingredient = Recipe.ingredients.get(name="pork butt")
        weight = UnitShifter().set_conversion_dict(ingredient)

        by_weight = UnitShifter().by_weight(ingredient, new_serving_size, weight)

        print "Holy crap. The oz dictionary to the right place."

    def test_method_conversion_dict_tsp(self):
        """The script applies the tsp conversion_dict to the by_volume method"""
        new_serving_size = 8
        ingredient = Recipe.ingredients.get(name="pineapple juice")
        volume = UnitShifter().set_conversion_dict(ingredient)

        by_volume = UnitShifter().by_volume(ingredient, new_serving_size, volume)

        print "Holy crap. The tsp dictionary to the right place."

    def test_by_weight_less_than_one(self):
        """Method by_weight properly handles a quantity of < 1"""

    def test_by_weight_low_integer(self):
        """Method by_weight handles a low integer properly"""

    def test_by_weight_high_integer(self):
        """Method by_weight handles a high integer properly"""

    def test_by_weight_float(self):
        """Method by_weight properly handles a float"""

    def test_by_volume_less_than_one(self):
        """Method by_volume properly handles a quantity of < 1"""

    def test_by_volume_low_integer(self):
        """Method by_volume handles a low integer properly"""

    def test_by_volume_high_integer(self):
        """Method by_volume handles a high integer properly"""

    def test_by_volume_float(self):
        """Method by_volume properly handles a float"""

    def test_ordered_dict_ordering(self):
        """Items in OrderedDict are ordered correctly"""

    def test_scale_volume_less_than_one(self):
        """Method scale_volume properly handles a value < 1"""

    def test_scale_volume_small_integer(self):
        """Method scale_volume properly handles a small integer"""

    def test_scale_volume_large_integer(self):
        """Method scale_volume properly handles a large integer"""

    def test_scale_volume_float(self):
        """Method scale_volume properly handles a float"""

    def test_scale_weight_less_than_one(self):
        """Method scale_weight properly handles a value < 1"""

    def test_scale_weight_small_integer(self):
        """Method scale_weight properly handles a small integer"""

    def test_scale_weight_large_integer(self):
        """Method scale_weight properly handles a large integer"""

    def test_scale_weight_float(self):
        """Method scale_weight properly handles a float"""
