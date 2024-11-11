from rest_framework import serializers
from .models import Book
from .utils import convert_currency_decimal_to_string
from decimal import Decimal

class CurrencyDecimalField(serializers.Field):
    def to_representation(self, value):
        # Convert Decimal value to string formatted as currency
        if isinstance(value, Decimal):
            return convert_currency_decimal_to_string(value)
        return None

class BookSerializer(serializers.HyperlinkedModelSerializer):
    published_date = serializers.DateField(format='%d-%m-%Y')
    price = CurrencyDecimalField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'price']
