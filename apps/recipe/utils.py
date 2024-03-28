from quantulum3 import parser


def parse_quantity_and_unit(ingredient):
    quantity = None
    unit = None

    # Parse the ingredient using quantulum3 parser
    quantities = parser.parse(ingredient)

    # Extract quantity and unit from the parsed result
    if quantities:
        quantity = quantities[0].value
        unit = quantities[0].unit.name

    return quantity, unit


def extract_ingredient_name(ingredient):
    # Parse the ingredient using quantulum3 parser
    quantities = parser.parse(ingredient)

    # If quantities are found, remove them from the ingredient string
    if quantities:
        ingredient = ingredient.replace(quantities[0].surface, '')

    # Remove leading and trailing whitespace and return the remaining text as the ingredient name
    return ingredient.strip()