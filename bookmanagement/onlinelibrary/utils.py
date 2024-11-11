##############################################################
# Define unit function for reuse purpose                     #
##############################################################
import string
from datetime import datetime
from decimal import Decimal
import re

expected_format = "%d-%m-%Y"

##############################################################
# input : string value                                       #
# output: True or False                                      #
# usage : To check if value contains special characters such #
# as !$%?                                                    #
##############################################################
def contains_special_characters(input_string):
    special_chars = string.punctuation
    return any(char in special_chars for char in input_string)

##############################################################
# data_integrety_lack_check(field_list, input_field)         #
# Returns the fields that are missing from input compared to #
# the expected field list (excluding 'id').                  #
##############################################################
def data_integrety_lack_check(field_list, input_field):
    return set(field_list) & (set(field_list) ^ set(input_field)) ^ {'id'}

##############################################################
# data_integrety_abundant_check(field_list, input_field)     #
# Returns the fields in input that are not in the expected   #
# field list (excluding 'id').                               #                #
##############################################################
def data_integrety_abundant_check(field_list, input_field):
    return set(input_field) & (set(field_list) ^ set(input_field))

##############################################################
# input : string of published_date (dd-mm-yyyy)              #
# output: string of published_date (yyyy-mm-dd)              #
# usage : To return database stored datetime format         #
##############################################################
def validate_publish_date(date_string):
    try:
        date_string = datetime.strptime(date_string, expected_format)
        
        return date_string.strftime("%Y-%m-%d")  
    except ValueError:
        return None

##############################################################
# input : decimal of price                                   #
# output: error                                              #
# usage : To check if price > 0 or not                       #
##############################################################
def validate_price(price_input):
    if price_input < 0:
        return 'price must bigger 0'
    else:
        return None
    
##############################################################
# expected input : 19,000.00 VND                             #
# output         : 19000.00                                  #
# usage          : To convert str -> decimal for database    #
#                  storage                                   #
##############################################################
def convert_currency_string_to_decimal(currency_string):
    try:
        cleaned_string = re.sub(r'[^\d.-]', '', currency_string)
        return Decimal(cleaned_string)
    except ValueError:
        return None

##############################################################
# input : decimal of price                                   #
# output: 19,000.00 VND                                      #
# usage : For client visibility                              #
##############################################################
def convert_currency_decimal_to_string(currency_decimal, currency_symbol="VND"):
    formatted_value = f"{currency_decimal:,.2f}"
    return f"{formatted_value} {currency_symbol}"