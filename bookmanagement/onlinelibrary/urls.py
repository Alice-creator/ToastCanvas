from django.urls import path
from . import apis
urlpatterns = [
    path('book/<int:id>', apis.BookRD),
    path('book', apis.BookCU),
]