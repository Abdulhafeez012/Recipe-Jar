import unittest
from apps.recipe.utils import (
    parse_quantity_and_unit,
    extract_ingredient_name,
    convert_recipe_fraction
)


class TestIngredientFunctions(unittest.TestCase):
    def test_parse_quantity_and_unit(self):
        ingredient = "2 ½ cup flour"
        quantity, unit = parse_quantity_and_unit(ingredient)
        self.assertEqual(quantity, 1)
        self.assertEqual(unit, "cup")

        ingredient = "1/2 teaspoon salt"
        quantity, unit = parse_quantity_and_unit(ingredient)
        self.assertEqual(quantity, 0.5)
        self.assertEqual(unit, "teaspoon")

        ingredient = "eggs"
        quantity, unit = parse_quantity_and_unit(ingredient)
        self.assertIsNone(quantity)
        self.assertIsNone(unit)

    def test_extract_ingredient_name(self):
        ingredient = "1 cup flour"
        name = extract_ingredient_name(ingredient)
        self.assertEqual(name, "flour")

        ingredient = "1/2 teaspoon salt"
        name = extract_ingredient_name(ingredient)
        self.assertEqual(name, "salt")

        ingredient = "eggs"
        name = extract_ingredient_name(ingredient)
        self.assertEqual(name, "eggs")

    def test_convert_fraction(self):
        ingredient = "1/2 teaspoon salt"
        converted_ingredient = convert_recipe_fraction(ingredient)
        self.assertEqual(converted_ingredient, "0.5 teaspoon salt")

        ingredient = "3/4 cup sugar"
        converted_ingredient = convert_recipe_fraction(ingredient)
        self.assertEqual(converted_ingredient, "0.75 cup sugar")

        ingredient = "1 cup flour"
        converted_ingredient = convert_recipe_fraction(ingredient)
        self.assertEqual(converted_ingredient, "1 cup flour")


if __name__ == '__main__':
    unittest.main()
