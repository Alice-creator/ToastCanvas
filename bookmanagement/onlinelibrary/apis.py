from django.http import JsonResponse
from rest_framework import status, response, decorators
from .models import Book
from .serializer import BookSerializer
import json
from .utils import *

##############################################################
# GET all books by id and send it to client                  #
##############################################################
@decorators.api_view(['GET'])
def BookAll(request):
    book = Book.objects.all()
    serializer = BookSerializer(book, many=True)
    return JsonResponse({'detail': serializer.data}, status=status.HTTP_200_OK)


##############################################################
# GET a book by id and send it to client                     #
# CASE covered:                                              #
# - id is not integer (Rest middleware covered)              #
# - id does not exist                                        #
##############################################################
##############################################################
# DELETE a book by id and send it to client                  #
# CASE covered:                                              #
# - id is not integer (Rest middleware covered)              #
# - id does not exist                                        #
##############################################################
@decorators.api_view(['GET', 'DELETE'])
def BookRD(request, id):
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
         return response.Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return JsonResponse({'detail': serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        book.delete()
        return response.Response({'detail': 'Record has been deleted'}, status=status.HTTP_200_OK)

##############################################################
# CREATE a book                                              #
# CASE covered:                                              #
# - Value contains special symbol                            #
# - Lacking of attributes in body                            #
# - Abundance of attributes in body                          #
# - Wrong published_date format                              #
# - Book's price < 0                                         #
# - Book is already exist                                    #
##############################################################
##############################################################
# UPDATE a book                                              #
# CASE covered:                                              #
# - Value contains special symbol                            #
# - Lacking of attributes in body                            #
# - Abundance of attributes in body                          #
# - Wrong published_date format                              #
# - Book's price < 0                                         #
# - Book is already exist                                    #
##############################################################
@decorators.api_view(['POST','PUT'])
def BookCU(request):
    data = json.loads(request.body)
    # Check values contain special symbol 
    for i in data:
        if contains_special_characters(str(data[i])) and i not in 'pricepublished_date':
            return response.Response({'detail': i + ' contains invalid character'}, status=status.HTTP_400_BAD_REQUEST)
    # Check lacking of attributes in body    
    loss_atts = list(data_integrety_lack_check([field.name for field in Book._meta.get_fields()], data.keys()))
    if len(loss_atts) > 0:
        return response.Response({'detail': ', '.join(map(str, loss_atts)) + ' are missing'}, status=status.HTTP_404_NOT_FOUND)

    # Check abundance of attributes in body
    abundant_atts = list(data_integrety_abundant_check([field.name for field in Book._meta.get_fields()], data.keys()))
    if len(abundant_atts) > 0:
        return response.Response({'detail': ', '.join(map(str, abundant_atts)) + ' are abundant'}, status=status.HTTP_400_BAD_REQUEST)

    # Check published_date format
    data['published_date'] = validate_publish_date(data['published_date'])
    if data['published_date'] == None:
        return response.Response({'detail': 'Invalid published date'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Convert string to decimal(price is decimal in database but user's input is string)
    data['price'] = convert_currency_string_to_decimal(data['price'])
    if data['price'] == None:
        return response.Response({'detail': 'Invalid price input'}, status=status.HTTP_400_BAD_REQUEST)
    # Check if price is negative
    message = validate_price(data['price'])
    if message != None:
        return response.Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'POST':
        try:
            book = Book.objects.get(isbn=data['isbn'])
            return response.Response({'detail': 'Book is already exist'}, status=status.HTTP_409_CONFLICT)
        except Book.DoesNotExist:
            Book.objects.create(**data)
            return response.Response({'detail': 'Book is inserted'}, status=status.HTTP_201_CREATED)
    elif request.method == 'PUT':
        try:
            book = Book.objects.get(isbn=data['isbn'])
            for key, value in data.items():
                setattr(book, key, value)
            book.save()
            return response.Response({'detail': 'Book is updated'}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return response.Response({'detail': 'Book is not exist'}, status=status.HTTP_404_NOT_FOUND)