##############################################################
# Serializer work as ORM                                     #
# Transform data from database into dictionary object        #
##############################################################

from rest_framework import serializers
from .models import Book
from .utils import convert_currency_decimal_to_string
from decimal import Decimal

##############################################################
# Price in Database is decimal                               #
# For visibility usage,                                      #
# we need price to be in specific format                     #
##############################################################
class CurrencyDecimalField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, Decimal):
            return convert_currency_decimal_to_string(value)
        return None

##############################################################
# When book JSON object sent to client                       #
# Attributes in fields variable will be shown                #
##############################################################
class BookSerializer(serializers.HyperlinkedModelSerializer):
    published_date = serializers.DateField(format='%d-%m-%Y')
    price = CurrencyDecimalField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'price']
