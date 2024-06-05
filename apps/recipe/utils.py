import re
import requests
from quantulum3 import parser
from bs4 import BeautifulSoup

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


def extract_time_duration(url):
    # Fetch the HTML content of the webpage
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the first text from the webpage
        first_text = soup.get_text().strip().split('\n')[0]

        # Define regular expressions to match time-related patterns
        time_patterns = [
            r'\b(\d+)\s*(?:min(?:ute)?s?)\b',
            r'\b(\d+)\s*(?:hour(?:s)?)\b',
            r'\b(\d+)\s*(?:h)\b',  # abbreviated form for hours
        ]

        # Search for time-related patterns in the first text
        for pattern in time_patterns:
            match = re.search(pattern, first_text, re.IGNORECASE)
            if match:
                return int(match.group(1))  # Extract the numerical value

    return None  # Return None if no time-related information is found
