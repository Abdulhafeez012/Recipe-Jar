import unittest
from apps.recipe.utils import (
    parse_quantity_and_unit,
    extract_ingredient_name,
    extract_time_duration,
)


class TestIngredientFunctions(unittest.TestCase):
    def test_parse_quantity_and_unit(self):
        ingredient = "2 ½ cup flour"
        quantity, unit = parse_quantity_and_unit(ingredient)
        self.assertEqual(quantity, 2.5)
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

    # def test_extract_time_duration(self):
    #     recipe = """
    #     Preheat the oven to 375 degrees. Cook the chicken for 45 minutes.
    #     Let it rest for 10 minutes before serving.
    #     Simmer the sauce for 1 hour and 30 minutes.
    #     """
    #     duration = extract_time_duration(recipe)
    #     self.assertEqual(duration, 145)
    #
    #     recipe = "Bake for 20 minutes. Let cool for 10 minutes."
    #     duration = extract_time_duration(recipe)
    #     self.assertEqual(duration, 30)
    #
    #     recipe = "Simmer for 1 hour. Let stand for 5 minutes."
    #     duration = extract_time_duration(recipe)
    #     self.assertEqual(duration, 65)
    #
    #     recipe = "Preheat the oven for 10 minutes, then bake for 35 minutes. Allow to rest for 15 minutes."
    #     duration = extract_time_duration(recipe)
    #     self.assertEqual(duration, 60)
    #
    #     recipe = "Boil the water for 2 minutes. Cook the pasta for 8-10 minutes. Let it rest for 5 minutes."
    #     duration = extract_time_duration(recipe)
    #     self.assertEqual(duration, 16)


if __name__ == '__main__':
    unittest.main()
