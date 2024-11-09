from django.http import JsonResponse
from rest_framework import status, response, decorators
from .models import Book
from django.shortcuts import get_object_or_404
import json
@decorators.api_view(['GET', 'DELETE'])
def BookRD(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'GET':
        return response.Response(book, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        book.delete()
        return response.Response({'detail': 'Record has been deleted'}, status=status.HTTP_200_OK)

@decorators.api_view(['POST','PUT'])
def BookCU(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        try:
            book = Book.objects.get(isbn=data['isbn'])
            return response.Response({'detail': 'Book is already exist'}, status=status.HTTP_409_CONFLICT)
        except Book.DoesNotExist:
            Book.objects.create(**data)
            return response.Response({'detail': 'Book is inserted'}, status=status.HTTP_201_CREATED)
    elif request.method == 'PUT':
        None