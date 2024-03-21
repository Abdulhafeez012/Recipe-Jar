import re
from fractions import Fraction


def parse_quantity_and_unit(ingredient):
    quantity = None
    unit = None

    # Updated regex pattern to match quantity and unit
    pattern = r'(?:(\d*\.?\d+)\s*(?:\/\s*(\d+))?\s*)(\w*)'
    match = re.search(pattern, ingredient)
    if match:
        quantity_whole_part = match.group(1)
        quantity_fraction_part = match.group(2)
        unit = match.group(3)
        # Construct quantity from whole part and fraction part
        if quantity_whole_part:
            quantity = float(quantity_whole_part)
            if quantity_fraction_part:
                quantity += float(Fraction('0.' + quantity_fraction_part))
    return quantity, unit


def extract_ingredient_name(ingredient):
    # Updated regex pattern to extract ingredient name
    pattern = r'^\s*(?:\d*\.?\d*\s*(?:\/\s*\d+)?\s*\w*)?\s*(.*)$'
    match = re.search(pattern, ingredient)
    if match:
        ingredient_name = match.group(1).strip()
        if ingredient_name:
            return ingredient_name
        # If no quantity or unit, return the entire ingredient as the name
        return ingredient.strip()


def fraction_to_decimal(match):
    # Convert fraction to decimal
    fraction_str = match.group(1)
    try:
        return str(float(Fraction(fraction_str)))
    except ValueError:
        return fraction_str


def convert_recipe_fraction(ingredient):
    # Replace fractions with decimal values
    fraction_pattern = r'(\d*\.?\d+\/\d+)'
    replaced = re.sub(fraction_pattern, fraction_to_decimal, ingredient)

    return replaced
