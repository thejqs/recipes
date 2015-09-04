from django.test import TestCase
from main.scripts.unit_shifter import UnitShifter

# Create your tests here.


class ShiftingUnitsTestCase(TestCase):

    def test_disallow_negatives(self):
        """Nothing runs if ingredient quantity is negative"""

    def test_conversion_dict(self):
        """The script chooses the correction conversion_dict for the ingredient type"""

    def test_method_conversion_dict(self):
        """The script applies the correct conversion_dict to the right method"""

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
