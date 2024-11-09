from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    published_date = models.DateField()
    isbn = models.CharField(unique=True, max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=15)