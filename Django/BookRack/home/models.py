from django.db import models
from  django.contrib.auth.models import User
from django.conf import settings

class Cart(models.Model):
    bookid=models.IntegerField()
    booktitle=models.CharField(max_length=255)
    price=models.IntegerField()
    quantity=models.IntegerField()
    imageurl=models.CharField(max_length=500)

class Interest(models.Model):
    
    userid=models.IntegerField()
    bookid=models.IntegerField()
    booktitle=models.CharField(max_length=255)
    bookgenres=models.CharField(max_length=500)
    bookauthor=models.CharField(max_length=200)
    bookdesc=models.CharField(max_length=5500)
    bookimage=models.CharField(max_length=500)
