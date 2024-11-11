import string
from datetime import datetime
from decimal import Decimal
import re

expected_format = "%d-%m-%Y"

def data_integrety_lack_check(field_list, input_field):
    return set(field_list) & (set(field_list) ^ set(input_field)) ^ {'id'}

def data_integrety_abundant_check(field_list, input_field):
    return set(input_field) & (set(field_list) ^ set(input_field))

def contains_special_characters(input_string):
    special_chars = string.punctuation
    return any(char in special_chars for char in input_string)

def validate_publish_date(date_string):
    try:
        date_string = datetime.strptime(date_string, expected_format)
        
        return date_string.strftime("%Y-%m-%d")  
    except ValueError:
        return None

def validate_price(price_input):
    if price_input < 0:
        return 'price must bigger 0'
    else:
        return None

def convert_currency_string_to_decimal(currency_string):
    # Remove the currency symbol and commas
    
    
    # Convert the cleaned string to a Decimal
    try:
        cleaned_string = re.sub(r'[^\d.-]', '', currency_string)
        return Decimal(cleaned_string)
    except ValueError:
        return None  # Return None if the conversion fails

def convert_currency_decimal_to_string(currency_decimal, currency_symbol="VND"):
    # Format the decimal value with commas for thousands and two decimal places
    formatted_value = f"{currency_decimal:,.2f}"
    
    # Add the currency symbol at the end
    return f"{formatted_value} {currency_symbol}"