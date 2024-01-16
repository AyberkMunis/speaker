from email.mime import base
from email.policy import default
from statistics import mode
from tkinter import Place
from unicodedata import name
from django.db import models
import string
import random

def generate_uniquecode():
    length=6
    while True:
        code="".join(random.choices(string.ascii_uppercase,k=length))
        if Place.objects.filter(code=code).count() ==0:
            break
    return code



# Create your models here.
class Place(models.Model):
    code=models.CharField(max_length=8,default=generate_uniquecode,unique=True)
    host=models.CharField(max_length=50,unique=True)
    genre=models.CharField(max_length=50,default='')
    base=models.CharField(max_length=500,default='')
    name=models.CharField(max_length=50,default='')
    taste=models.JSONField(default={})
    created_at=models.DateTimeField(auto_now_add=True)
    current_song = models.CharField(max_length=50, null=True)


